from __future__ import annotations

from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path

DEFAULT_PORT = 4
DEFAULT_BAUDRATE = 9600
DEFAULT_THEM = 1


@dataclass
class AppConfig:
    com_port: int = DEFAULT_PORT
    baudrate: int = DEFAULT_BAUDRATE
    address: int = 1
    mask: int = 1
    light_control: bool = False
    track_bar: bool = False
    them: int = DEFAULT_THEM

    @property
    def port_name(self) -> str:
        """Возвращает имя COM-порта в формате COMx."""
        return f"COM{self.com_port}"

    def to_public_dict(self) -> dict[str, object]:
        """Преобразует конфигурацию в словарь для передачи на фронтенд."""
        return {
            "com_port": self.com_port,
            "port_name": self.port_name,
            "baudrate": self.baudrate,
            "address": self.address,
            "mask": self.mask,
            "light_control": self.light_control,
            "track_bar": self.track_bar,
            "them": 1 if int(self.them) == 1 else 0,
        }


def _read_bool(value: str | None, fallback: bool = False) -> bool:
    """Безопасно читает булево значение из строки с fallback по умолчанию."""
    if value is None:
        return fallback
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _read_int(value: str | None, fallback: int) -> int:
    """Безопасно читает целое число из строки с fallback при ошибке."""
    if value is None:
        return fallback
    try:
        return int(value.strip())
    except (TypeError, ValueError):
        return fallback


def _read_them(value: str | None, fallback: int = DEFAULT_THEM) -> int:
    """Читает параметр темы и нормализует его к диапазону 0/1."""
    parsed = _read_int(value, fallback)
    return 1 if parsed == 1 else 0


def load_app_config(config_path: Path) -> AppConfig:
    """Загружает настройки приложения из config.ini в структуру AppConfig."""
    parser = ConfigParser()
    if config_path.exists():
        try:
            parser.read(config_path, encoding="cp1251")
        except UnicodeDecodeError:
            parser.read(config_path, encoding="utf-8")

    port_raw = parser.get("Port", "Com", fallback=str(DEFAULT_PORT))
    baud_raw = parser.get("Port", "Baudrate", fallback=str(DEFAULT_BAUDRATE))
    address_raw = parser.get("Admin", "Address", fallback="1")
    mask_raw = parser.get("Admin", "Mask", fallback="1")
    light_raw = parser.get("Admin", "LightControl", fallback="0")
    track_raw = parser.get("Admin", "TrackBar", fallback="0")
    them_raw = parser.get(
        "Admin",
        "Theme",
        fallback=parser.get("Admin", "Them", fallback=str(DEFAULT_THEM)),
    )

    return AppConfig(
        com_port=_read_int(port_raw, DEFAULT_PORT),
        baudrate=_read_int(baud_raw, DEFAULT_BAUDRATE),
        address=_read_int(address_raw, 1),
        mask=_read_int(mask_raw, 1),
        light_control=_read_bool(light_raw, False),
        track_bar=_read_bool(track_raw, False),
        them=_read_them(them_raw, DEFAULT_THEM),
    )


def save_app_config(config_path: Path, cfg: AppConfig) -> None:
    """Сохраняет текущие настройки приложения в config.ini."""
    them_value = 1 if int(cfg.them) == 1 else 0

    parser = ConfigParser()
    parser["Port"] = {
        "Com": str(cfg.com_port),
        "Baudrate": str(cfg.baudrate),
    }
    parser["Admin"] = {
        "Address": str(cfg.address),
        "Mask": str(cfg.mask),
        "LightControl": "1" if cfg.light_control else "0",
        "TrackBar": "1" if cfg.track_bar else "0",
        "Theme": str(them_value),
    }

    config_path.parent.mkdir(parents=True, exist_ok=True)

    with config_path.open("w", encoding="cp1251", newline="\n") as file:
        parser.write(file)
