from __future__ import annotations

import asyncio
import calendar
import logging
import math
import os
import re
import shutil
import sys
import threading
import time
import webbrowser
from datetime import datetime
from functools import wraps
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Callable, Coroutine
import eel

try:
    import pystray  
    from PIL import Image, ImageDraw 
except Exception:
    pystray = None
    Image = None
    ImageDraw = None

from backend import DeviceService, list_available_ports, load_app_config, save_app_config

APP_DIR = Path(__file__).resolve().parent
IS_FROZEN = "__compiled__" in globals()

if IS_FROZEN:
    # В onefile-конфигурации сохраняем пользовательский ini рядом с exe.
    PROJECT_DIR = Path(sys.argv[0]).resolve().parent
else:
    # При запуске из IDE - рядом со скриптом
    PROJECT_DIR = APP_DIR

WEB_DIR = APP_DIR / "web"
CONFIG_PATH = PROJECT_DIR / "config.ini"
COMMANDS_PATH = PROJECT_DIR / "commands.ini"
BUNDLED_CONFIG_PATH = APP_DIR / "config.ini"
BUNDLED_COMMANDS_PATH = APP_DIR / "commands.ini"
LOG_FILE_NAME = "plc_nova.log"
APP_HOST = "127.0.0.1"
APP_PORT = 8123
APP_SIZE = (1460, 920)
PORTS_CACHE_TTL_SECONDS = 3600.0


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def _resolve_cache_dir() -> Path:
    """Возвращает папку runtime-кэша с fallback в директорию проекта."""
    local_app_data = Path(os.environ.get("LOCALAPPDATA", str(PROJECT_DIR)))
    candidates = [
        local_app_data / "PLC_Nova" / "cache",
        PROJECT_DIR / ".plc_nova_cache",
    ]
    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            return candidate
        except OSError:
            continue

    fallback = PROJECT_DIR / ".plc_nova_cache"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


RUNTIME_CACHE_DIR = _resolve_cache_dir()
CHROME_PROFILE_DIR = RUNTIME_CACHE_DIR / "chrome_profile"

TIME_PATTERN = re.compile(
    r"TIME[=\s](?P<time>\d{2}:\d{2}:\d{2})\s+DAY[=\s]?(?P<day>\d)\s+DATE[=\s]?(?P<date>\d{2}\.\d{2}\.\d{2})",
    re.IGNORECASE,
)

GEO_PATTERN = re.compile(
    r"Lat=(?P<lat>\d{3})\s+Lon=(?P<lon>\d{3})\s+Zone=\s*(?P<zone>\d{1,2})",
    re.IGNORECASE,
)

BITS_PATTERN = re.compile(r"^(?P<kind>KEYS|MASK)=(?P<bits>[01]{3})$", re.IGNORECASE)
SCHEDULE_PATTERN = re.compile(
    r"^(?P<index>\d{2})\s+(?P<active>[01])\s+(?P<days>[01]{7})\s+"
    r"(?:"
    r"(?P<time_type_compact>[0-2])(?P<sign_compact>[+-])(?P<hours_compact>\d{2}):(?P<minutes_compact>\d{2})"
    r"|"
    r"(?P<time_type_split>[0-2])\s+(?P<hours_split>\d{2}):(?P<minutes_split>\d{2})"
    r")\s+"
    r"(?P<address>\d{3})\s+(?P<command>\d{3})(?:\s+(?P<level>\d{3,4}))?$"
)


def _resolve_log_path() -> Path:
    """Возвращает путь к лог-файлу в папке logs рядом со скриптом."""
    print(f"[LOG] APP_FILE: {__file__}")
    print(f"[LOG] APP_DIR: {APP_DIR}")
    print(f"[LOG] PROJECT_DIR: {PROJECT_DIR}")
    logs_dir = APP_DIR / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / LOG_FILE_NAME
    
    print(f"[LOG] Log path: {log_path}")
    return log_path

LOG_PATH = _resolve_log_path()


def _configure_logging() -> logging.Logger:
    """Инициализирует ротационный лог-файл для диагностики."""
    # Используем конкретный logger для app - не propagate
    logger = logging.getLogger("plc_nova.app")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.handlers = []  # Очищаем старые handlers
    
    file_handler = RotatingFileHandler(
        LOG_PATH,
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )
    logger.addHandler(file_handler)
    
    return logger


APP_LOGGER = _configure_logging()


class AsyncRunner:
    def __init__(self) -> None:
        """Создает отдельный asyncio-цикл в фоновой нити для вызовов из Eel."""
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def _run_loop(self) -> None:
        """Запускает бесконечный цикл обработки асинхронных задач."""
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def run(self, coroutine: Coroutine[Any, Any, Any]) -> Any:
        """Безопасно выполняет корутину в фоновом цикле и возвращает результат."""
        future = asyncio.run_coroutine_threadsafe(coroutine, self._loop)
        return future.result()


runner = AsyncRunner()
device = DeviceService()
app_config = load_app_config(CONFIG_PATH)
_ports_cache: list[str] = []
_ports_cache_ts = 0.0


def _run(coroutine: Coroutine[Any, Any, Any]) -> Any:
    """Короткий прокси для запуска корутин через AsyncRunner."""
    return runner.run(coroutine)


def _normalize_port_name(port_name: str) -> str:
    """Нормализует имя порта к виду COMx и валидирует формат."""
    raw = str(port_name).strip().upper()
    if not raw:
        raise ValueError("Не указан COM-порт (пример: COM4)")

    suffix = raw[3:] if raw.startswith("COM") else raw
    if not suffix.isdigit():
        raise ValueError("Порт должен быть в формате COM4 или 4")
    return f"COM{int(suffix)}"


def _extract_port_number(port_name: str) -> int:
    """Возвращает номер COM-порта как целое число."""
    return int(_normalize_port_name(port_name)[3:])


def _normalize_them_value(value: Any) -> int:
    """Преобразует входное значение темы к формату Theme: 1 (светлая) или 0 (темная)."""
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Theme должен быть 1 (светлая) или 0 (темная)") from exc
    if parsed not in (0, 1):
        raise ValueError("Theme должен быть 1 (светлая) или 0 (темная)")
    return parsed


def _load_command_templates(path: Path, limit: int = 120) -> list[str]:
    """Загружает шаблоны команд из ini-файла для подсказок в UI."""
    if not path.exists():
        return []

    result: list[str] = []
    with path.open("r", encoding="cp1251", errors="ignore") as file:
        for raw_line in file:
            command = raw_line.split(";", 1)[0].strip()
            if not command:
                continue
            result.append(command)
            if len(result) >= limit:
                break
    return result


def _get_ports_cached(force_refresh: bool = False) -> list[str]:
    """Возвращает список портов из кэша, чтобы ускорить повторное открытие окна."""
    global _ports_cache, _ports_cache_ts

    now = time.monotonic()
    cache_expired = (now - _ports_cache_ts) > PORTS_CACHE_TTL_SECONDS

    if force_refresh or cache_expired or not _ports_cache:
        _ports_cache = list_available_ports()
        _ports_cache_ts = now

    return list(_ports_cache)


def _resolve_commands_path() -> Path:
    """Возвращает путь к commands.ini: внешний рядом с exe или встроенный."""
    if COMMANDS_PATH.exists():
        return COMMANDS_PATH
    if BUNDLED_COMMANDS_PATH.exists():
        return BUNDLED_COMMANDS_PATH
    return COMMANDS_PATH


def _ensure_runtime_config_file() -> None:
    """Гарантирует наличие config.ini рядом с exe/проектом."""
    global app_config

    if CONFIG_PATH.exists():
        return

    # Если есть встроенный шаблон config.ini (например, в onefile), используем его.
    if BUNDLED_CONFIG_PATH.exists() and BUNDLED_CONFIG_PATH != CONFIG_PATH:
        app_config = load_app_config(BUNDLED_CONFIG_PATH)

    save_app_config(CONFIG_PATH, app_config)


_ensure_runtime_config_file()


def _clear_runtime_cache() -> None:
    """Автоматически очищает runtime-кэш приложения при запуске."""
    global _ports_cache, _ports_cache_ts

    _ports_cache = []
    _ports_cache_ts = 0.0

    try:
        if CHROME_PROFILE_DIR.exists():
            shutil.rmtree(CHROME_PROFILE_DIR, ignore_errors=True)
        CHROME_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        APP_LOGGER.warning("Runtime cache cleanup failed: %s", exc)


def _find_last_line(lines: list[str], prefixes: tuple[str, ...]) -> str:
    """Ищет последнюю строку ответа, начинающуюся с одного из префиксов."""
    for line in reversed(lines):
        if any(line.startswith(prefix) for prefix in prefixes):
            return line
    return ""


def _parse_time_line(line: str) -> dict[str, object]:
    """Разбирает строку TIME в структурированный словарь."""
    match = TIME_PATTERN.search(line)
    if not match:
        raise ValueError(f"Не удалось разобрать ответ TIME: {line}")
    return {
        "time": match.group("time"),
        "day": int(match.group("day")),
        "date": match.group("date"),
    }


def _parse_geo_line(line: str) -> dict[str, object]:
    """Разбирает строку GEONEZ в словарь координат и часового пояса."""
    match = GEO_PATTERN.search(line)
    if not match:
        raise ValueError(f"Не удалось разобрать ответ GEONEZ: {line}")
    return {
        "lat": int(match.group("lat")),
        "lon": int(match.group("lon")),
        "zone": int(match.group("zone")),
    }


def _parse_bits_line(line: str, expected_kind: str) -> dict[str, object]:
    """Разбирает ответы KEYS/MASK и переводит биты в булевы поля."""
    match = BITS_PATTERN.match(line.strip())
    if not match:
        raise ValueError(f"Не удалось разобрать ответ {expected_kind}: {line}")

    kind = match.group("kind").upper()
    if kind != expected_kind:
        raise ValueError(f"Ожидался ответ {expected_kind}, получено: {line}")

    bits = match.group("bits")
    return {
        "raw": line,
        "a": bits[0] == "1",
        "b": bits[1] == "1",
        "c": bits[2] == "1",
        "bits": bits,
    }


def _parse_schedule(lines: list[str]) -> list[dict[str, object]]:
    """Преобразует текстовый ответ SHED в список структурированных записей."""
    entries: list[dict[str, object]] = []
    for line in lines:
        match = SCHEDULE_PATTERN.match(line.strip())
        if not match:
            continue

        # Контроллеры встречаются в двух форматах времени:
        # 1) compact: "2-00:10" (тип+знак+время)
        # 2) split:   "0 00:05"  (для fixed-time без явного знака)
        if match.group("time_type_compact") is not None:
            time_type = int(match.group("time_type_compact"))
            sign = match.group("sign_compact") or "+"
            hours = match.group("hours_compact")
            minutes = match.group("minutes_compact")
        else:
            time_type = int(match.group("time_type_split"))
            # Некоторые версии контроллера отдают fixed-time как "0 00:00" без знака.
            sign = "+"
            hours = match.group("hours_split")
            minutes = match.group("minutes_split")

        days = match.group("days")
        level_raw = match.group("level")
        entries.append(
            {
                "index": int(match.group("index")),
                "active": match.group("active") == "1",
                "days": [day == "1" for day in days],
                "time_type": time_type,
                "sign": sign,
                "time": f"{hours}:{minutes}",
                "address": int(match.group("address")),
                "command": int(match.group("command")),
                "level": int(level_raw) if level_raw is not None else 0,
                "raw": line,
            }
        )

    def _entry_index(entry: dict[str, object]) -> int:
        """Извлекает индекс строки расписания для корректной сортировки."""
        value = entry.get("index", 0)
        return value if isinstance(value, int) else int(str(value))

    entries.sort(key=_entry_index)
    return entries


def _as_bool(value: Any) -> bool:
    """Нормализует разные типы значений в bool."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _bits_from_values(a: Any, b: Any, c: Any) -> str:
    """Собирает битовую маску из трех значений для команд KEYS/MASK."""
    return "".join("1" if _as_bool(bit) else "0" for bit in (a, b, c))


def _parse_optional_int(value: Any) -> int | None:
    """Читает опциональное целое значение из поля формы."""
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None
    return int(text)


def _resolve_address(ai: Any = None, ag: Any = None) -> int:
    """Преобразует адрес AI/AG к протокольному формату с проверкой диапазонов."""
    ai_value = _parse_optional_int(ai)
    ag_value = _parse_optional_int(ag)

    # Если AG заполнен, он имеет приоритет над AI.
    if ag_value is not None:
        if not (0 <= ag_value <= 29):
            raise ValueError("Групповой адрес AG должен быть в диапазоне 0..29")
        return 0 if ag_value == 0 else 220 + ag_value

    if ai_value is None:
        raise ValueError("Укажите AI (1..220) или AG (0..29)")
    if not (1 <= ai_value <= 220):
        raise ValueError("Индивидуальный адрес AI должен быть в диапазоне 1..220")
    return ai_value


def _normalize_channel(channel: str) -> str:
    """Нормализует название спектрального канала к внутреннему ключу."""
    normalized = str(channel).strip().lower().replace(" ", "").replace("_", "")
    mapping = {
        "red": "red",
        "blue": "blue",
        "farred": "farred",
        "far-red": "farred",
        "white": "white",
    }
    if normalized not in mapping:
        raise ValueError("Канал должен быть одним из: red, blue, farred, white")
    return mapping[normalized]


def _scale_percent_for_scene(value: Any) -> int:
    """Переводит проценты мощности канала в шкалу команд старого протокола."""
    percent = int(value)
    if not (0 <= percent <= 100):
        raise ValueError("Процент канала должен быть в диапазоне 0..100")
    if percent == 0:
        return 0
    if percent <= 10:
        return 1
    return (percent // 5) - 1


def _send_command_burst(
    command: str,
    attempts: int = 1,
    gap_seconds: float = 0.0,
    timeout: float = 0.35,
    max_lines: int = 32,
    expect_response: bool = False,
) -> list[str]:
    """Отправляет команду несколько раз подряд с паузой между попытками."""
    safe_attempts = max(1, int(attempts))
    merged_lines: list[str] = []

    for index in range(safe_attempts):
        lines = _run(
            device.send_command(
                command,
                timeout=timeout,
                max_lines=max_lines,
                expect_response=expect_response and (index == safe_attempts - 1),
            )
        )
        if lines:
            merged_lines.extend(lines)

        if index < safe_attempts - 1 and gap_seconds > 0:
            time.sleep(gap_seconds)

    return merged_lines


def _build_channel_command_code(channel: str, percent: Any) -> tuple[str, int, int]:
    """Строит код команды канала (140..219) по имени канала и проценту."""
    channel_name = _normalize_channel(channel)
    percent_value = int(percent)
    scaled = _scale_percent_for_scene(percent_value)
    base_codes = {
        "red": 140,
        "blue": 160,
        "farred": 180,
        "white": 200,
    }
    command_code = base_codes[channel_name] + scaled
    return channel_name, percent_value, command_code


def _build_schedule_days(days: Any) -> str:
    """Формирует семибитную маску дней недели для SHED-команды."""
    if isinstance(days, str):
        compact = "".join(char for char in days if char in "01")
        if len(compact) != 7:
            raise ValueError("Строка дней должна содержать ровно 7 бит")
        return compact

    if not isinstance(days, list) or len(days) != 7:
        raise ValueError("Поле дней должно содержать список из 7 значений")
    return "".join("1" if _as_bool(item) else "0" for item in days)


def _build_schedule_command(payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Собирает и валидирует строку SHED= из данных формы редактора."""
    index = int(payload.get("index", 0))
    # По фактической логике PLT_1 и ответам контроллера используются строки 00..19.
    if not (0 <= index <= 19):
        raise ValueError("Индекс расписания должен быть в диапазоне 0..19")

    active = _as_bool(payload.get("active", True))
    days_bits = _build_schedule_days(payload.get("days", [True, True, True, True, True, True, True]))

    time_type = int(payload.get("time_type", 0))
    if time_type not in (0, 1, 2):
        raise ValueError("time_type должен быть 0 (фикс), 1 (рассвет) или 2 (закат)")

    sign = str(payload.get("sign", "+")).strip() or "+"
    if sign not in {"+", "-"}:
        raise ValueError("sign должен быть '+' или '-'")
    if time_type == 0:
        sign = "+"

    hours = int(payload.get("hours", 0))
    minutes = int(payload.get("minutes", 0))
    if not (0 <= hours <= 23):
        raise ValueError("Часы должны быть в диапазоне 0..23")
    if not (0 <= minutes <= 59):
        raise ValueError("Минуты должны быть в диапазоне 0..59")

    target_mode = str(payload.get("target_mode", "ai")).strip().lower()
    diag_level: int | None = None

    if target_mode == "keys":
        address = 250
        key_a = _as_bool(payload.get("key_a", False))
        key_b = _as_bool(payload.get("key_b", False))
        key_c = _as_bool(payload.get("key_c", False))
        command_code = (1 if key_a else 0) + (2 if key_b else 0) + (4 if key_c else 0)
    elif target_mode == "diag":
        address = 251
        key_a = _as_bool(payload.get("key_a", False))
        key_b = _as_bool(payload.get("key_b", False))
        key_c = _as_bool(payload.get("key_c", False))
        # Совместимость с PLT_1 (Unit10): для DIAG команда всегда 000,
        # а биты A/B/C кодируются в поле level как 100/010/001.
        command_code = 0
        diag_level = (100 if key_a else 0) + (10 if key_b else 0) + (1 if key_c else 0)
    elif target_mode == "ai":
        address = _resolve_address(payload.get("ai"), payload.get("ag"))

        brightness = _parse_optional_int(payload.get("brightness"))
        scene = _parse_optional_int(payload.get("scene"))
        command_direct = _parse_optional_int(payload.get("command_code"))

        selected = [item is not None for item in (brightness, scene, command_direct)]
        if selected.count(True) != 1:
            raise ValueError("Укажите ровно одно поле: brightness, scene или command_code")

        if brightness is not None:
            if not (0 <= brightness <= 10):
                raise ValueError("brightness должен быть в диапазоне 0..10")
            command_code = brightness
        elif scene is not None:
            if not (1 <= scene <= 20):
                raise ValueError("scene должен быть в диапазоне 1..20")
            command_code = 10 + scene
        else:
            if command_direct is None or not (0 <= command_direct <= 255):
                raise ValueError("command_code должен быть в диапазоне 0..255")
            command_code = command_direct
    else:
        raise ValueError("target_mode должен быть ai, keys или diag")

    level = int(payload.get("level", 0))
    if not (0 <= level <= 9999):
        raise ValueError("level должен быть в диапазоне 0..9999")
    if diag_level is not None:
        level = diag_level

    # Совместимость с PLT_1: level в SHED пишется только при LightControl или DIAG.
    include_level = bool(app_config.light_control) or (diag_level is not None)

    command_base = (
        f"SHED={index:02d} {1 if active else 0} {days_bits} "
        f"{time_type}{sign}{hours:02d}:{minutes:02d} "
        f"{address:03d} {command_code:03d}"
    )
    command = f"{command_base} {level:04d}" if include_level else command_base

    return command, {
        "index": index,
        "active": active,
        "days": [char == "1" for char in days_bits],
        "time_type": time_type,
        "sign": sign,
        "time": f"{hours:02d}:{minutes:02d}",
        "address": address,
        "command": command_code,
        "level": level,
    }


def _normalize_360(value: float) -> float:
    """Нормализует угол в диапазон 0..360 градусов."""
    result = value
    while result > 360:
        result -= 360
    while result < 0:
        result += 360
    return result


def _hour_to_hm(value: float) -> tuple[int, int]:
    """Переводит дробные часы в пару (часы, минуты)."""
    result = value
    while result > 24:
        result -= 24
    while result < 0:
        result += 24
    hours = int(result)
    minutes = int((result - hours) * 60.0)
    return hours, minutes


def _sun_calc(day: int, month: int, year: int, desired: int, lat: int, lon: int, zone: int) -> tuple[int, int]:
    """Вычисляет время рассвета или заката по координатам и дате."""
    rad = math.pi / 180
    zenith = 96.0

    day_of_year = (
        math.floor((275 * month) / 9)
        - math.floor((month + 9) / 12) * (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
        + day
        - 30
    )

    lng_hour = lon / 15
    if desired == 0:
        approx_time = day_of_year + ((6 - lng_hour) / 24)
    else:
        approx_time = day_of_year + ((18 - lng_hour) / 24)

    mean_anomaly = (0.9856 * approx_time) - 3.289
    true_long = mean_anomaly + (1.916 * math.sin(mean_anomaly * rad)) + (0.02 * math.sin(2 * mean_anomaly * rad)) + 282.634
    true_long = _normalize_360(true_long)

    right_ascension = math.degrees(math.atan(0.91764 * math.tan(true_long * rad)))
    l_quadrant = math.floor(true_long / 90) * 90
    ra_quadrant = math.floor(right_ascension / 90) * 90
    right_ascension = (right_ascension + (l_quadrant - ra_quadrant)) / 15

    sin_dec = 0.39782 * math.sin(true_long * rad)
    cos_dec = math.cos(math.asin(sin_dec))
    cos_h = (math.cos(zenith * rad) - (sin_dec * math.sin(lat * rad))) / (cos_dec * math.cos(lat * rad))

    if cos_h > 1:
        return 66, 0
    if cos_h < -1:
        return 99, 0

    if desired == 0:
        local_hour = 360 - math.degrees(math.acos(cos_h))
    else:
        local_hour = math.degrees(math.acos(cos_h))
    local_hour = local_hour / 15

    local_time = local_hour + right_ascension - (0.06571 * approx_time) - 6.622 - lng_hour + zone
    return _hour_to_hm(local_time)


def _apply_minute_correction(hours: int, minutes: int, correction: int) -> tuple[int, int]:
    """Применяет минутную коррекцию к времени с циклическим переходом через сутки."""
    total = hours * 60 + minutes + correction
    while total < 0:
        total += 24 * 60
    while total >= 24 * 60:
        total -= 24 * 60
    return total // 60, total % 60


def _api_guard(function: Callable[..., Any]) -> Callable[..., dict[str, object]]:
    """Оборачивает API-метод в единый формат ответа {ok,data/error}."""
    @eel.expose
    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> dict[str, object]:
        """Безопасно выполняет API-функцию и перехватывает исключения."""
        try:
            if function.__name__ not in {"api_get_logs", "api_trace_log"}:
                APP_LOGGER.info("API call: %s", function.__name__)
            data = function(*args, **kwargs)
            return {"ok": True, "data": data}
        except Exception as exc:
            APP_LOGGER.exception("API error in %s: %s", function.__name__, exc)
            return {"ok": False, "error": str(exc)}

    return wrapper


@_api_guard
def api_bootstrap() -> dict[str, object]:
    """Возвращает стартовые данные приложения для первичной инициализации UI."""
    return {
        "config": app_config.to_public_dict(),
        "connection": device.get_connection_state(),
        "ports": _get_ports_cached(force_refresh=True),
        "command_templates": _load_command_templates(_resolve_commands_path()),
        "log_file": str(LOG_PATH),
    }


@_api_guard
def api_trace_log(message: str) -> dict[str, object]:
    """Записывает отладочную строку UI в общий лог приложения."""
    text = str(message).strip()
    if text:
        APP_LOGGER.info("TRACE | %s", text)
    return {"message": text}


@_api_guard
def api_set_theme(them: Any) -> dict[str, object]:
    """Сохраняет параметр Theme: 1 для светлой темы, 0 для темной."""
    app_config.them = _normalize_them_value(them)
    save_app_config(CONFIG_PATH, app_config)
    return {"them": app_config.them}


@_api_guard
def api_refresh_ports() -> list[str]:
    """Обновляет список доступных COM-портов."""
    return _get_ports_cached(force_refresh=True)


@_api_guard
def api_connect(port_name: str, baudrate: int) -> dict[str, object]:
    """Подключает приложение к контроллеру и сохраняет параметры соединения."""
    port = _normalize_port_name(port_name or app_config.port_name)
    speed = int(baudrate)
    if speed <= 0:
        raise ValueError("Скорость baudrate должна быть положительной")

    app_config.com_port = _extract_port_number(port)
    app_config.baudrate = speed
    save_app_config(CONFIG_PATH, app_config)

    state = _run(device.connect(port, speed))

    warning = ""
    try:
        _run(device.send_command("TIME", expected_prefixes=("TIME=", "TIME "), timeout=2.8))
    except Exception as exc:
        warning = (
            "Порт открыт, но ответа от контроллера нет. "
            "Проверьте RS-485 в свойствах COM (драйвер CP210x), "
            "полярность A/B и соответствие baudrate. "
            f"Детали: {exc}"
        )
        APP_LOGGER.warning("Connection probe TIME failed for %s @ %s: %s", port, speed, exc)

    if warning:
        state["warning"] = warning
    return state


@_api_guard
def api_disconnect() -> dict[str, object]:
    """Разрывает текущее соединение с контроллером."""
    return _run(device.disconnect())


@_api_guard
def api_save_connection(port_name: str, baudrate: int) -> dict[str, object]:
    """Сохраняет настройки COM-порта в config.ini без подключения к устройству."""
    port = _normalize_port_name(port_name or app_config.port_name)
    speed = int(baudrate)
    if speed <= 0:
        raise ValueError("Скорость baudrate должна быть положительной")

    app_config.com_port = _extract_port_number(port)
    app_config.baudrate = speed
    save_app_config(CONFIG_PATH, app_config)
    return app_config.to_public_dict()


@_api_guard
def api_read_time() -> dict[str, object]:
    """Считывает текущее время контроллера по команде TIME."""
    lines = _run(device.send_command("TIME", expected_prefixes=("TIME=", "TIME ")))
    time_line = _find_last_line(lines, ("TIME=", "TIME "))
    if not time_line:
        raise RuntimeError("Ответ TIME не найден")

    parsed = _parse_time_line(time_line)
    parsed["raw"] = time_line
    parsed["lines"] = lines
    return parsed


@_api_guard
def api_set_time(time_value: str, day_value: int, date_value: str) -> dict[str, object]:
    """Записывает время, день недели и дату в контроллер."""
    if not re.fullmatch(r"\d{2}:\d{2}:\d{2}", str(time_value).strip()):
        raise ValueError("Время должно быть в формате ЧЧ:ММ:СС")

    day = int(day_value)
    if day < 1 or day > 7:
        raise ValueError("DAY должен быть в диапазоне 1..7")

    if not re.fullmatch(r"\d{2}\.\d{2}\.\d{2}", str(date_value).strip()):
        raise ValueError("Дата должна быть в формате ДД.ММ.ГГ")

    command = f"TIME {time_value.strip()} DAY={day} DATE={date_value.strip()}"
    lines = _run(device.send_command(command))
    return {"command": command, "lines": lines}


@_api_guard
def api_sync_local_time() -> dict[str, object]:
    """Синхронизирует часы контроллера с локальным временем ПК."""
    now = datetime.now()
    command = (
        f"TIME {now.strftime('%H:%M:%S')} "
        f"DAY={now.isoweekday()} "
        f"DATE={now.strftime('%d.%m.%y')}"
    )
    lines = _run(device.send_command(command))
    return {"command": command, "lines": lines}


@_api_guard
def api_read_geo() -> dict[str, object]:
    """Считывает географические координаты и часовой пояс из контроллера."""
    lines = _run(device.send_command("GEONEZ", expected_prefixes=("Lat=",)))
    line = _find_last_line(lines, ("Lat=",))
    if not line:
        raise RuntimeError("Ответ GEONEZ не найден")

    parsed = _parse_geo_line(line)
    parsed["raw"] = line
    parsed["lines"] = lines
    return parsed


@_api_guard
def api_set_geo(lat: int, lon: int, zone: int) -> dict[str, object]:
    """Записывает географические координаты и часовой пояс в контроллер."""
    lat_value = int(lat)
    lon_value = int(lon)
    zone_value = int(zone)

    if not (35 <= lat_value <= 74):
        raise ValueError("Широта должна быть в диапазоне 35..74")
    if not (20 <= lon_value <= 160):
        raise ValueError("Долгота должна быть в диапазоне 20..160")
    if not (0 <= zone_value <= 12):
        raise ValueError("Часовой пояс должен быть в диапазоне 0..12")

    command = f"GEONEZ={lat_value:03d},{lon_value:03d},{zone_value:02d}"
    lines = _run(device.send_command(command))
    return {"command": command, "lines": lines}


@_api_guard
def api_read_keys() -> dict[str, object]:
    """Считывает состояние битов KEYS из контроллера."""
    lines = _run(device.send_command("KEYS", expected_prefixes=("KEYS=",)))
    line = _find_last_line(lines, ("KEYS=",))
    if not line:
        raise RuntimeError("Ответ KEYS не найден")

    parsed = _parse_bits_line(line, "KEYS")
    parsed["lines"] = lines
    return parsed


@_api_guard
def api_set_keys(a: Any, b: Any, c: Any) -> dict[str, object]:
    """Записывает состояние битов KEYS в контроллер."""
    bits = _bits_from_values(a, b, c)
    command = f"KEYS={bits}"
    lines = _run(device.send_command(command))
    return {"command": command, "bits": bits, "lines": lines}


@_api_guard
def api_read_mask() -> dict[str, object]:
    """Считывает маску каналов MASK из контроллера."""
    lines = _run(device.send_command("MASK", expected_prefixes=("MASK=",)))
    line = _find_last_line(lines, ("MASK=",))
    if not line:
        raise RuntimeError("Ответ MASK не найден")

    parsed = _parse_bits_line(line, "MASK")
    parsed["lines"] = lines
    return parsed


@_api_guard
def api_set_mask(a: Any, b: Any, c: Any) -> dict[str, object]:
    """Записывает маску каналов MASK в контроллер."""
    bits = _bits_from_values(a, b, c)
    command = f"MASK={bits}"
    lines = _run(device.send_command(command))
    return {"command": command, "bits": bits, "lines": lines}


@_api_guard
def api_send_com(address: int, command_code: int) -> dict[str, object]:
    """Отправляет базовую команду COM с адресом и кодом."""
    address_value = int(address)
    command_value = int(command_code)

    if not (0 <= address_value <= 255):
        raise ValueError("Адрес должен быть в диапазоне 0..255")
    if not (0 <= command_value <= 255):
        raise ValueError("Код команды должен быть в диапазоне 0..255")

    command = f"COM {address_value:03d},{command_value:03d}"
    lines = _run(
        device.send_command(
            command,
            timeout=0.35,
            max_lines=32,
            expect_response=False,
        )
    )
    return {"command": command, "lines": lines}


@_api_guard
def api_enable_address_programming() -> dict[str, object]:
    """Включает режим программирования адреса через команду ADRPRG=1."""
    command = "ADRPRG=1"
    lines = _run(device.send_command(command))
    return {"command": command, "lines": lines}


@_api_guard
def api_set_ai_address(ai: int) -> dict[str, object]:
    """Записывает новый индивидуальный адрес устройства командой COM 255,AAA."""
    ai_value = int(ai)
    if not (1 <= ai_value <= 220):
        raise ValueError("Адрес AI должен быть в диапазоне 1..220")
    command = f"COM 255,{ai_value:03d}"
    lines = _run(device.send_command(command))
    return {"command": command, "ai": ai_value, "lines": lines}


@_api_guard
def api_assign_group_slot(ai: Any, ag: Any, slot: int, group_number: int, clear: Any = False) -> dict[str, object]:
    """Назначает или очищает групповой слот AG0..AG5 по логике старого Unit3."""
    address = _resolve_address(ai, ag)

    if _as_bool(clear):
        code = 230
    else:
        slot_value = int(slot)
        group_value = int(group_number)
        if not (0 <= slot_value <= 5):
            raise ValueError("Слот группы должен быть в диапазоне 0..5")
        if not (0 <= group_value <= 29):
            raise ValueError("Номер группы должен быть в диапазоне 0..29")

        code = 50 + 30 * slot_value + group_value
        if code == 50:
            raise ValueError("Для слота AG0 значение 0 недопустимо")

    command = f"COM {address:03d},{code:03d}"
    lines = _run(device.send_command(command))
    return {
        "command": command,
        "address": address,
        "code": code,
        "cleared": _as_bool(clear),
        "lines": lines,
    }


@_api_guard
def api_send_brightness(
    ai: Any,
    ag: Any,
    brightness: Any = None,
    scene: Any = None,
    command_code: Any = None,
) -> dict[str, object]:
    """Управляет яркостью/сценой или сервисной командой через модуль COM."""
    address = _resolve_address(ai, ag)

    brightness_value = _parse_optional_int(brightness)
    scene_value = _parse_optional_int(scene)
    command_value = _parse_optional_int(command_code)
    selected = [item is not None for item in (brightness_value, scene_value, command_value)]

    if selected.count(True) != 1:
        raise ValueError("Укажите ровно одно поле: brightness, scene или command_code")

    if brightness_value is not None:
        if not (0 <= brightness_value <= 10):
            raise ValueError("Яркость должна быть в диапазоне 0..10")
        code = brightness_value
    elif scene_value is not None:
        if not (1 <= scene_value <= 20):
            raise ValueError("Номер сцены должен быть в диапазоне 1..20")
        code = 10 + scene_value
    else:
        if command_value is None or not (230 <= command_value <= 250):
            raise ValueError("command_code должен быть в диапазоне 230..250")
        code = command_value

    command = f"COM {address:03d},{code:03d}"
    lines = _run(
        device.send_command(
            command,
            timeout=0.35,
            max_lines=32,
            expect_response=False,
        )
    )
    return {"command": command, "address": address, "code": code, "lines": lines}


@_api_guard
def api_scene_activate(ai: Any, ag: Any, scene: int) -> dict[str, object]:
    # === Scene (COMA) APIs ===
    # These APIs control scene activation, saving and per-channel scene edits
    # using legacy COMA command encodings. Kept as fire-and-forget where
    # appropriate to match device behaviour.
    """Активирует выбранный номер сценария по команде COMA."""
    address = _resolve_address(ai, ag)
    scene_value = int(scene)
    if not (1 <= scene_value <= 20):
        raise ValueError("Сцена должна быть в диапазоне 1..20")
    code = 10 + scene_value
    command = f"COMA{address:03d},{code:03d}"

    # Для broadcast (000) отправляем команду дважды: это повышает шанс,
    # что все устройства на шине применят воспроизведение сцены.
    if address == 0:
        lines = _send_command_burst(
            command,
            attempts=2,
            gap_seconds=0.35,
            timeout=0.35,
            max_lines=32,
            expect_response=False,
        )
    else:
        lines = _run(
            device.send_command(
                command,
                timeout=0.35,
                max_lines=32,
                expect_response=False,
            )
        )

    return {"command": command, "lines": lines}


@_api_guard
def api_scene_save(ai: Any, ag: Any, scene: int) -> dict[str, object]:
    # Save current luminaire spectrum to numbered scene (COMA 30+N).
    """Сохраняет текущее состояние каналов в номер сценария."""
    address = _resolve_address(ai, ag)
    scene_value = int(scene)
    if not (1 <= scene_value <= 20):
        raise ValueError("Сцена должна быть в диапазоне 1..20")
    code = 30 + scene_value
    command = f"COMA{address:03d},{code:03d}"

    # Для broadcast (000) дублируем команду записи сцены.
    # Последнюю попытку выполняем с ожиданием ответа, чтобы UI видел OK.
    if address == 0:
        lines = _send_command_burst(
            command,
            attempts=2,
            gap_seconds=0.5,
            timeout=1.5,
            max_lines=64,
            expect_response=True,
        )
    else:
        lines = _run(
            device.send_command(
                command,
                timeout=1.5,
                max_lines=64,
                expect_response=True,
            )
        )

    normalized_lines = [str(line).strip() for line in (lines or []) if str(line).strip()]
    has_ok = any(line.upper().startswith("OK") for line in normalized_lines)
    has_prompt = any(line == ">" for line in normalized_lines)

    if not has_ok:
        if has_prompt:
            normalized_lines.insert(0, "OK")
        elif not normalized_lines:
            normalized_lines = ["OK"]

    return {"command": command, "lines": normalized_lines}


@_api_guard
def api_scene_set_start(ai: Any, ag: Any) -> dict[str, object]:
    # Configure device start-up scene (COMA ... ,220)
    """Записывает стартовый сценарий, который включается при подаче питания."""
    address = _resolve_address(ai, ag)
    command = f"COMA{address:03d},220"
    lines = _run(
        device.send_command(
            command,
            timeout=0.35,
            max_lines=32,
            expect_response=False,
        )
    )
    # Дополнительная пауза после входа в режим программирования сцен.
    # Контроллеру требуется время на переключение в режим записи.
    time.sleep(0.5)
    return {"command": command, "lines": lines}


@_api_guard
def api_scene_set_channel(
    ai: Any,
    ag: Any,
    channel: str,
    percent: int,
    wait_response: Any = False,
) -> dict[str, object]:
    # Per-channel scene editing API: maps percent->legacy scene codes and
    # sends COMA commands for the specific spectral channel.
    """Настраивает мощность отдельного спектрального канала в процентах."""
    address = _resolve_address(ai, ag)
    channel_name, percent_value, code = _build_channel_command_code(channel, percent)

    command = f"COMA{address:03d},{code:03d}"

    # В legacy PLT_1 команды COMA-каналов отправляются без ожидания ответа.
    # На части контроллеров ACK не приходит стабильно, и ожидание вызывает
    # ложные таймауты и ухудшает запись полного спектра перед SAVE.
    requested_wait_response = _as_bool(wait_response)
    wait_for_response = False

    if address == 0:
        # Для broadcast (000) отправляем каждый спектральный канал серией,
        # чтобы команды доехали до всех устройств на общей линии.
        lines = _send_command_burst(
            command,
            attempts=3,
            gap_seconds=0.55,
            timeout=0.35,
            max_lines=32,
            expect_response=False,
        )
        settle_delay = 0.55
        channel_timeout = 0.35
    else:
        channel_timeout = 1.1 if requested_wait_response else 0.5
        settle_delay = 0.35 if requested_wait_response else 0.15
        lines = _run(
            device.send_command(
                command,
                timeout=channel_timeout,
                max_lines=64 if requested_wait_response else 32,
                expect_response=False,
            )
        )

    # Небольшая пауза после каждой команды канала для стабильности
    time.sleep(settle_delay)
    return {
        "command": command,
        "channel": channel_name,
        "percent": percent_value,
        "scaled": code % 20,
        "transport": "COMA",
        "mode": "scene_programming",
        "wait_response_requested": requested_wait_response,
        "wait_response": wait_for_response,
        "code": code,
        "address": address,
        "broadcast_burst": address == 0,
        "requested_address": {"ai": _parse_optional_int(ai), "ag": _parse_optional_int(ag)},
        "lines": lines,
    }


@_api_guard
def api_scene_assign_group(ai: Any, ag: Any, slot: int, group_number: int) -> dict[str, object]:
    """Назначает групповой адрес в один из слотов AG0/AG1/AG2."""
    address = _resolve_address(ai, ag)
    slot_value = int(slot)
    group_value = int(group_number)
    if slot_value not in (1, 2, 3):
        raise ValueError("slot должен быть 1, 2 или 3")
    if not (1 <= group_value <= 29):
        raise ValueError("group_number должен быть в диапазоне 1..29")

    base_codes = {1: 50, 2: 80, 3: 110}
    code = base_codes[slot_value] + group_value
    command = f"COMA{address:03d},{code:03d}"
    lines = _run(
        device.send_command(
            command,
            timeout=0.35,
            max_lines=32,
            expect_response=False,
        )
    )
    return {"command": command, "lines": lines}


@_api_guard
def api_write_schedule_entry(payload: dict[str, Any]) -> dict[str, object]:
    """Записывает одну строку расписания в формате SHED=."""
    if not isinstance(payload, dict):
        raise ValueError("payload должен быть JSON-объектом")
    command, entry = _build_schedule_command(payload)
    lines = _run(device.send_command(command, timeout=3.0, max_lines=260))
    return {
        "command": command,
        "entry": entry,
        "lines": lines,
    }


@_api_guard
def api_generate_astronomy(
    lat: int,
    lon: int,
    zone: int,
    year: int | None = None,
    morning_correction: int = 0,
    evening_correction: int = 0,
) -> dict[str, object]:
    """Генерирует годовую таблицу астрономических событий и сохраняет txt/csv."""
    lat_value = int(lat)
    lon_value = int(lon)
    zone_value = int(zone)
    year_value = int(year) if year is not None else datetime.now().year
    morning_corr = int(morning_correction)
    evening_corr = int(evening_correction)

    if not (35 <= lat_value <= 74):
        raise ValueError("Широта должна быть в диапазоне 35..74")
    if not (20 <= lon_value <= 160):
        raise ValueError("Долгота должна быть в диапазоне 20..160")
    if not (0 <= zone_value <= 12):
        raise ValueError("Часовой пояс должен быть в диапазоне 0..12")
    if not (2000 <= year_value <= 2100):
        raise ValueError("Год должен быть в диапазоне 2000..2100")
    if not (-120 <= morning_corr <= 120):
        raise ValueError("Поправка рассвета должна быть в диапазоне -120..120")
    if not (-120 <= evening_corr <= 120):
        raise ValueError("Поправка заката должна быть в диапазоне -120..120")

    txt_path = PROJECT_DIR / "astronony.txt"
    csv_path = PROJECT_DIR / "astronony.csv"

    month_labels = [
        "Jan.", "Feb.", "Mar.", "Apr.", "May", "June",
        "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec.",
    ]

    text_lines = [
        f"                                           Calculation Civil Twilight for {year_value}",
        f"                        Location: East {lon_value}, North {lat_value}  Time Zone +{zone_value}h East of Greenwich",
        "",
        "       " + "       ".join(f"{label:<10}" for label in month_labels),
        "Day Begin End  Begin End  Begin End  Begin End  Begin End  Begin End  Begin End  Begin End  Begin End  Begin End  Begin End  Begin End",
        "     h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m",
    ]

    csv_lines: list[str] = []
    total_work_minutes = 0

    for day in range(1, 32):
        text_row = f"{day:02d}"
        csv_row = f"{day:02d};"
        for month in range(1, 13):
            _, month_days = calendar.monthrange(year_value, month)
            if day > month_days:
                text_row += "           "
                csv_row += "00;00;00;00;"
                continue

            sunrise_h, sunrise_m = _sun_calc(day, month, year_value, 0, lat_value, lon_value, zone_value)
            sunrise_h, sunrise_m = _apply_minute_correction(sunrise_h, sunrise_m, morning_corr)

            sunset_h, sunset_m = _sun_calc(day, month, year_value, 1, lat_value, lon_value, zone_value)
            sunset_h, sunset_m = _apply_minute_correction(sunset_h, sunset_m, evening_corr)

            total_work_minutes += sunrise_h * 60 + sunrise_m
            total_work_minutes += 24 * 60 - (sunset_h * 60 + sunset_m)

            text_row += f"  {sunrise_h:02d}{sunrise_m:02d} {sunset_h:02d}{sunset_m:02d}"
            csv_row += f"{sunrise_h:02d};{sunrise_m:02d};{sunset_h:02d};{sunset_m:02d};"

        text_lines.append(text_row)
        csv_lines.append(csv_row)

    total_work_hours = total_work_minutes // 60
    text_lines.append(f" Total minutes: {total_work_minutes}  Total hours: {total_work_hours}")

    txt_path.write_text("\n".join(text_lines) + "\n", encoding="utf-8")
    csv_path.write_text("\n".join(csv_lines) + "\n", encoding="utf-8")

    return {
        "text_file": txt_path.name,
        "csv_file": csv_path.name,
        "year": year_value,
        "lat": lat_value,
        "lon": lon_value,
        "zone": zone_value,
        "morning_correction": morning_corr,
        "evening_correction": evening_corr,
        "total_minutes": total_work_minutes,
        "total_hours": total_work_hours,
    }


@_api_guard
def api_send_raw(command: str) -> dict[str, object]:
    """Отправляет произвольную команду протокола и возвращает полный ответ."""
    normalized = str(command).strip()
    if not normalized:
        raise ValueError("Команда не может быть пустой")

    uppercase = normalized.upper()
    fire_and_forget = uppercase.startswith("COM ") or uppercase.startswith("COMA")
    lines = _run(
        device.send_command(
            normalized,
            timeout=0.35 if fire_and_forget else 3.0,
            max_lines=260,
            expect_response=not fire_and_forget,
        )
    )
    schedule = _parse_schedule(lines) if normalized.upper() == "SHED" else []
    return {
        "command": normalized,
        "lines": lines,
        "schedule": schedule,
    }


@_api_guard
def api_read_schedule() -> dict[str, object]:
    """Считывает расписание SHED из контроллера и разбирает его в таблицу."""
    lines = _run(
        device.send_command(
            "SHED",
            expected_prefixes=("FILTER",),
            timeout=4.5,
            max_lines=260,
        )
    )
    entries = _parse_schedule(lines)
    return {
        "count": len(entries),
        "entries": entries,
        "lines": lines,
    }


@_api_guard
def api_get_logs(limit: int = 200) -> dict[str, object]:
    """Возвращает последние записи протокольного журнала для отображения."""
    return {"items": device.get_logs(int(limit))}


@_api_guard
def api_get_connection_state() -> dict[str, object]:
    """Возвращает актуальное состояние подключения."""
    return device.get_connection_state()


# === AI Agent API ===

_agent_instance = None


def _get_agent():
    """Ленивая инициализация агента."""
    global _agent_instance
    if _agent_instance is None:
        try:
            sys.path.insert(0, str(APP_DIR))
            from agent.main import PLCAgent
            _agent_instance = PLCAgent(device)
            _agent_instance.load_tools()
            _agent_instance.load_skills()
            _agent_instance.check_models()
            _agent_instance.check_speech()
            APP_LOGGER.info("AI Agent initialized with shared device")
        except Exception as exc:
            APP_LOGGER.exception("Failed to initialize AI Agent: %s", exc)
            raise
    return _agent_instance


@_api_guard
def api_agent_status() -> dict[str, object]:
    """Возвращает статус AI-агента."""
    APP_LOGGER.info("=== api_agent_status() called ===")
    try:
        agent = _get_agent()
        status = agent.get_status()
        APP_LOGGER.info("Status: %s", status)
        return status
    except Exception as exc:
        APP_LOGGER.exception("AI Agent status failed: %s", exc)
        return {
            "models_available": False,
            "speech_available": False,
            "lm_studio_available": False,
            "error": str(exc),
        }


@_api_guard
def api_agent_execute(command: str, reasoning: str = None) -> dict[str, object]:
    """Выполняет команду пользователя через AI-агента."""
    APP_LOGGER.info("=== api_agent_execute() called ===")
    APP_LOGGER.info("Command: %s, reasoning: %s", command, reasoning)
    
    agent = _get_agent()
    
    status = agent.get_status()
    APP_LOGGER.info("Agent status: lm_studio=%s, model_key=%s", 
                    status.get("lm_studio_available"), status.get("current_model"))
    
    system_prompt = """Ты - помощник для управления PLC-контроллерами освещения.
Ты общительный и дружелюбный, всегда стремишься помочь пользователю достичь желаемого результата.
Твоя задача: преобразовать запрос пользователя в команду(ы) протокола PLC или отвечать на вопросы пользователя.
Если дана команда, тогда:
ВЫВОДИ ТОЛЬКО СТАТУС И КОМАНДУ, без размышлений. Например: ВЫПОЛНЕНО: COMA000,011 - ЭТО ВАЖНО!
Если пользовтаель задает вопрос, приветсвие или ведет разговор на другие темы не связанные с командами контроллерва, тогда отвечай кратко, по существу, без излишних деталей и размышлений. Всегда сохраняй фокус на том, чтобы помочь пользователю с его запросом.
Например если пользователь спрашивает: Как настроить расписание? выводи команду для чтения и установки расписания с описанием параметров и так для всех команд.
ВАЖНО: ВСЕГДА ОТВЕТЧАЙ НА РУССКОМ ЯЗЫКЕ. ОТВЕЧАЙ НА ДРУГИХ ЯЗЫКАХ ТОЛЬКО ЕСЛИ ПОЛЬЗОВАТЕЛЬ ЯВНО ОБРАТИТСЯ К ТЕБЕ НА ЭТОМ ЯЗЫКЕ. НЕ ПЕРЕХОДИ НА АНГЛИЙСКИЙ, ЕСЛИ НЕ ПРОСЯТ. ТАКЖЕ ВСЕГДА ДЕЛАЙ КРАСИВЫЙ И ПОНЯТНЫЙ ВЫВОД!
ВАЖНО: НИКОГДА НЕ ВЫВОДИ ЧТО-ТО ТИПА: Приветствие/разговор: Пользователь прислал приветствие и команду. Нужно выполнить команду. ИЛИ Ответ должен быть только в формате статуса и команды. НЕ ПИШИ И НЕ ВЫВОДИ СВОИ РАЗМЫШЛЕНИЯ!
САМОЕ ВАЖНОЕ: НЕ ВЫПОЛНЯЙ НИКАИХ КОМАНД ЕСЛИ ТЕБЯ ЯВНО ОБ ЭТОМ НЕ ПРОСЯТ! НАПРИМЕР "Привет" ЭТО НЕ КОМАНДА!
Пример: Привет! Выполни сценарий 1.

Твой ответ должен быть: Привет! Выполняю команду! Стататус: ВЫПОЛНЕНО: COMA000,011

===== КОМАНДЫ ПРОТОКОЛА (формат COMA000,CCC - адрес 000 для broadcast) =====

1. ВЫКЛЮЧЕНИЕ ВСЕХ СВЕТИЛЬНИКОВ (самая важная!)
   Запрос: "выключи все", "выключи свет", "выключи всё"
   Формат: нужно отправить 4 КОМАНДЫ (для каждого канала):
   COMA000,140 COMA000,160 COMA000,180 COMA000,200
   (140=красный, 160=синий, 180=дальний красный, 200=белый)

2. СЦЕНЫ (воспроизведение сцены)
   Запрос: "сцена 1", "включи сценарий 1", "запусти сцену 5"
   Формат: COMA000,010+N (N=1..20)
   Пример: сцена 1 -> COMA000,011 (010+1=011)
   Пример: сцена 5 -> COMA000,015 (010+5=015)

3. ЯРКОСТЬ (управление яркостью, 0=выкл, 10=макс)
   Запрос: "яркость 5", "включи свет", "свет на 50%"
   Формат: канал 140+N (0=выкл, 10=макс)
   Пример: яркость 10 -> COMA000,149 (140+9=149 для 100%)
   Пример: яркость 5 -> COMA000,144 (50% -> 1)
   Пример: яркость 0 -> COMA000,140 (выключено)

4. ОТДЕЛЬНЫЕ КАНАЛЫ СПЕКТРА (ОДНА команда!)
   Красный (BASE=140): "красный 50%", "красный на полную"
   Синий (BASE=160): "синий 50%", "синий на полную"
   Белый (BASE=200): "белый 50%", "белый на полную"
   Дальний красный (BASE=180): "дальний красный 50%"
   
   ФОРМУЛА: COMA000,BASE+S
   S = 0 (для 0%), 1 (для 1-10%), для 11-100%: S = процент/5 - 1
   Пример: красный 20% -> S = 20/5 - 1 = 3 -> COMA000,143
   Пример: белый 40% -> S = 40/5 - 1 = 7 -> COMA000,207
   Пример: белый на полную (100%) -> S = 100/5 - 1 = 19 -> COMA000,219

5. ЧТЕНИЕ ДАННЫХ
   Время: "который час?", "время" -> TIME
   Ключи: "какие ключи?", "keys" -> KEYS
   Маска: "маска", "mask" -> MASK
   Геолокация: "координаты", "гео" -> GEONEZ
   Расписание: "расписание", "shed" -> SHED

6. ЗАПИСЬ СЦЕНЫ (N=1..20)
   Запрос: "запиши сцену 5"
   Формат: COMA000,030+N
   Пример: записать сцену 5 -> COMA000,035 (030+5=035)

===== ПРИМЕРЫ ======
"выключи всё" -> COMA000,140 COMA000,160 COMA000,180 COMA000,200
"сцена 1" -> COMA000,011
"яркость 10" -> COMA000,149
"красный 20%" -> COMA000,143
"белый 40%" -> COMA000,207
"белый на полную" -> COMA000,219
"""
    
    # Специальные вопросы - не через LM Studio
    cmd_lower = command.lower()
    if "порт" in cmd_lower or "com порт" in cmd_lower or "какие порты" in cmd_lower:
        # Прямой запрос списка портов
        from backend.device import list_available_ports
        ports = list_available_ports()
        if ports:
            port_list = ", ".join(ports)
            return {"success": True, "text": f"Доступные COM-порты: {port_list}", "action_result": {"ports": ports}}
        else:
            return {"success": True, "text": "COM-порты не обнаружены. Проверьте подключение USB-адаптера.", "action_result": {"ports": []}}
    
    if status.get("lm_studio_available") and status.get("current_model"):
        response_text = agent.generate_response(command, system_prompt, reasoning)
        APP_LOGGER.info("Model full response: '%s'", response_text)
        
        # Парсим ответ - ищем PLC команду(ы) в тексте
        import re
        cmd_pattern = r'(COMA0{3},\d{3}|COM0{3},\d{3}|TIME|KEYS|MASK|GEONEZ|SHED)'
        response_text = response_text or ""
        matches = re.findall(cmd_pattern, response_text, re.IGNORECASE)
        
        if matches:
            plc_command = " ".join(matches)
        else:
            lines = [line.strip() for line in (response_text or "").strip().split('\n') if line.strip()]
            plc_command = lines[-1] if lines else command
        
        APP_LOGGER.info("Extracted PLC command: '%s'", plc_command)
        
        # Проверяем - это PLC команда? Если содержит COMA/COM/TIME и т.д.
        is_plc_command = "COMA" in plc_command or "COM" in plc_command.upper() or plc_command.upper() in ["TIME", "KEYS", "MASK", "GEONEZ", "SHED"]
        
        # Выполняем команду если это PLC команда
        if is_plc_command:
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Выполняем команду
                APP_LOGGER.info("Executing PLC command from model: '%s'", plc_command)
                result = loop.run_until_complete(agent.execute(plc_command))
                loop.close()
                
                # Проверяем требует ли команда подключения
                if result.get("requires_connection"):
                    # В реальном режиме без подключения - показываем приглашение
                    if not getattr(agent, "test_mode", False):
                        return {
                            "success": True,
                            "text": "Привет! Пожалуйста подключитесь к COM порту, чтобы я мог выполнить команду!",
                            "action_result": result
                        }
                    else:
                        # В тестовом режиме - это ошибка
                        return {
                            "success": False, 
                            "text": response_text, 
                            "error": "Нет подключения к контроллеру. Подключитесь к COM-порту.",
                            "action_result": result
                        }
                
                return {"success": result.get("success", True), "text": response_text, "action_result": result}
            except Exception as exc:
                APP_LOGGER.error("Agent execute error: %s", exc)
                return {"success": False, "text": response_text, "action_result": {"error": str(exc)}}
        
        # Если не PLC команда - это чат
        return {"success": True, "text": response_text, "action_result": {"type": "chat", "success": True}}
    else:
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(agent.execute(command))
            loop.close()
            return result
        except Exception as exc:
            APP_LOGGER.error("Agent execute error: %s", exc)
            return {"success": False, "error": str(exc)}


@_api_guard
def api_agent_load_model(model_key: str, config: dict = None) -> dict[str, object]:
    """Загружает модель в LM Studio."""
    APP_LOGGER.info("=== api_agent_load_model() called ===")
    APP_LOGGER.info("model_key=%s, config=%s", model_key, config)
    
    agent = _get_agent()
    
    if not model_key:
        return {"success": False, "error": "Не указан ключ модели"}
    
    success = agent.load_model(model_key, config)
    APP_LOGGER.info("load_model result: %s", success)
    
    if success:
        return {"success": True, "message": f"Модель {model_key} загружена"}
    else:
        return {"success": False, "error": "Не удалось загрузить модель. Проверьте что LM Studio запущен."}


@_api_guard
def api_agent_unload_model() -> dict[str, object]:
    """Выгружает модель из памяти."""
    agent = _get_agent()
    agent.unload_model()
    return {"success": True, "message": "Модель выгружена"}


@_api_guard
def api_agent_clear_history() -> dict[str, object]:
    """Очищает историю чата."""
    agent = _get_agent()
    agent.clear_chat_history()
    return {"success": True, "message": "История очищена"}


@_api_guard
def api_agent_set_test_mode(enabled: bool) -> dict[str, object]:
    """Включает или выключает тестовый режим агента."""
    APP_LOGGER.info("=== api_agent_set_test_mode() called: enabled=%s ===", enabled)
    agent = _get_agent()
    agent.set_test_mode(enabled)
    return {"success": True, "test_mode": enabled}

@_api_guard
def api_agent_refresh_models() -> dict[str, object]:
    """Обновляет список доступных моделей из LM Studio."""
    APP_LOGGER.info("=== api_agent_refresh_models() called ===")
    agent = _get_agent()
    
    # Перезагружаем список моделей
    agent.check_models()
    models = agent.list_model_files()
    
    APP_LOGGER.info("Refreshed models: %d", len(models))
    return {"success": True, "models": models}
    

@_api_guard
def api_voice_recognize(audio_data: str, sample_rate: int = 16000) -> dict[str, object]:
    """Распознаёт речь из аудио данных через Google Speech Recognition."""
    APP_LOGGER.info("=== api_voice_recognize() called ===")
    
    agent = _get_agent()
    
    if not agent.speech_available:
        APP_LOGGER.warning("Speech recognition not available")
        return {"success": False, "error": "SpeechRecognition не доступен"}

    try:
        import base64
        wav_bytes = base64.b64decode(audio_data)
        APP_LOGGER.info("Processing %d bytes of audio", len(wav_bytes))
        text = agent.recognize_speech(wav_bytes)
        
        if text:
            APP_LOGGER.info("Recognized: %s", text)
            return {"success": True, "transcript": text}
        else:
            APP_LOGGER.warning("No speech detected")
            return {"success": False, "error": "Речь не распознана"}
    except Exception as exc:
        APP_LOGGER.error("Voice recognition error: %s", exc)
        return {"success": False, "error": str(exc)}


def _eel_close_callback(page: str, sockets: list[object]) -> None:
    """Сохраняет работу приложения после закрытия окна, чтобы оно оставалось в трее."""
    _ = (page, sockets)


def _run_eel_server() -> None:
    """Запускает Eel-сервер и GUI-окно, которое можно повторно открыть из трея."""
    options = {
        "host": APP_HOST,
        "port": APP_PORT,
        "size": APP_SIZE,
        "app_mode": True,
        # Отключаю HTTP-кэш в хроме и инструктируем сервер не кэшировать ответы
        "cmdline_args": [
            "--disable-http-cache",
            "--disable-application-cache",
            "--disk-cache-size=1",
            "--media-cache-size=1",
            f"--user-data-dir={CHROME_PROFILE_DIR}",
        ],
        "disable_cache": True,
        "close_callback": _eel_close_callback,
    }

    try:
        APP_LOGGER.info("Starting Eel server at http://%s:%s", APP_HOST, APP_PORT)
        eel.start("index.html", mode="chrome", **options)
    except (EnvironmentError, OSError):
        APP_LOGGER.warning("Chrome mode failed, switching to default browser mode")
        eel.start("index.html", mode="default", **options)


def _open_from_tray(icon: object = None, item: object = None) -> None:
    """Открывает окно приложения из пункта меню трея."""
    _ = (icon, item)
    try:
        APP_LOGGER.info("Tray action: open window")
        eel.show("index.html")
    except Exception:
        APP_LOGGER.warning("Eel window reopen failed, opening via system browser")
        webbrowser.open(f"http://{APP_HOST}:{APP_PORT}/index.html")


def _close_windows_before_exit() -> None:
    """Просит фронтенд закрыть окно перед завершением приложения."""
    try:
        close_window = getattr(eel, "tray_close_window", None)
        if callable(close_window):
            close_window()
            eel.sleep(0.2)
    except Exception:
        pass


def _exit_from_tray(icon: object, item: object) -> None:
    """Завершает приложение по команде из меню трея."""
    _ = item
    try:
        APP_LOGGER.info("Tray action: exit application")
        _close_windows_before_exit()
        stop_method = getattr(icon, "stop", None)
        if callable(stop_method):
            stop_method()
    finally:
        os._exit(0)


def _create_fallback_tray_image() -> object:
    """Создает простую иконку трея, если внешний файл иконки недоступен."""
    if Image is None or ImageDraw is None:
        raise RuntimeError("Для режима трея требуется Pillow")

    image = Image.new("RGBA", (64, 64), (19, 37, 58, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((8, 8, 56, 56), fill=(15, 106, 169, 255))
    draw.rectangle((20, 18, 44, 46), fill=(255, 255, 255, 220))
    return image


def _load_tray_image() -> object:
    """Загружает иконку для системного трея из файлов проекта."""
    if Image is None:
        raise RuntimeError("Для режима трея требуется Pillow")

    candidates = [
        PROJECT_DIR / "app_icon.ico",
        PROJECT_DIR / "logo_rus.png",
        PROJECT_DIR / "logo_eng.jpg",
    ]

    for candidate in candidates:
        if candidate.exists():
            try:
                return Image.open(candidate)
            except Exception:
                continue

    return _create_fallback_tray_image()


def _run_tray() -> None:
    """Запускает системный трей с пунктами «Открыть» и «Выйти»."""
    if pystray is None:
        raise RuntimeError("Для режима трея требуется пакет pystray")

    tray_image = _load_tray_image()
    tray_menu = pystray.Menu(
        pystray.MenuItem("Открыть", _open_from_tray, default=True),
        pystray.MenuItem("Выйти", _exit_from_tray),
    )
    tray_icon = pystray.Icon("plc_nova_console", tray_image, "PLC Nova Console", tray_menu)
    tray_icon.run()


def start() -> None:
    """Инициализирует Eel и запускает приложение с поддержкой системного трея."""
    APP_LOGGER.info("Application start. project_dir=%s config=%s log=%s", PROJECT_DIR, CONFIG_PATH, LOG_PATH)
    _clear_runtime_cache()
    
    # Устанавливаем переменную окружения для AI-агента (чтобы знал где искать модели)
    import os
    os.environ['APP_BASE_DIR'] = str(PROJECT_DIR)
    APP_LOGGER.info("APP_BASE_DIR set to: %s", PROJECT_DIR)
    
    eel.init(str(WEB_DIR))

    if pystray is None or Image is None:
        _run_eel_server()
        return

    server_thread = threading.Thread(target=_run_eel_server, daemon=True, name="eel-server")
    server_thread.start()
    _run_tray()


if __name__ == "__main__":
    start()

