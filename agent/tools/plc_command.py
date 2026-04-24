"""
PLC Command Tool - инструмент для отправки команд контроллеру PLC.
Поддерживает все протоколы: COM, COMA, TIME, GEONEZ, KEYS, MASK, SHED.
Парсит естественный язык в команды PLC.

Тестовый режим: если device.test_mode = True, команды не отправляются реально,
а просто логируются и возвращается заглушка.
"""
from __future__ import annotations

import asyncio
import logging
import re
from typing import Any, Optional

from backend.device import DeviceService

# Импортируем базовый класс Tool из agent.main
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import Tool

LOGGER = logging.getLogger("plc_nova.agent.tools.plc_command")


class PlcCommandTool(Tool):
    """
    Инструмент для отправки произвольных команд PLC-контроллеру.
    
    Поддерживаемые команды:
    - TIME / TIME=... - чтение/запись времени
    - GEONEZ / GEONEZ=... - географические координаты
    - KEYS / KEYS=... - биты KEYS
    - MASK / MASK=... - маска каналов
    - COM AAA,CCC - универсальная команда
    - COMA AAA,CCC - команда сценаиев/спектра
    - ЯРКОСТЬ N - яркость (0-10)
    - СЦЕНА N - активация сцены (1-20)
    - ВЫКЛЮЧИТЬ ВСЁ - выключение всех спектров
    - ВСЕ_СПЕКТРЫ N - все спектральные каналы на N%
    
    Тестовый режим: если device.test_mode = True, команды не отправляются реально,
    а просто логируются и возвращается заглушка.
    """
    
    def __init__(self, device: DeviceService) -> None:
        super().__init__(device, name="plc_command")
        self.test_mode = False  # Можно включить для тестов
    
    def get_schema(self) -> dict[str, Any]:
        """Возвращает схему параметров инструмента."""
        return {
            "name": self.name,
            "description": "Отправка команды PLC-контроллеру через COM-порт",
            "parameters": {
                "command": {
                    "type": "string",
                    "description": "Команда протокола (TIME, COM, COMA, и т.д.)",
                    "required": True
                },
                "timeout": {
                    "type": "number",
                    "description": "Таймаут ожидания ответа в секундах",
                    "default": 2.0
                },
                "expect_response": {
                    "type": "boolean",
                    "description": "Ожидать ли ответ от устройства",
                    "default": True
                }
            },
            "examples": [
                {"command": "TIME"},
                {"command": "COM 001,010"},
                {"command": "COMA001,220"},
                {"command": "GEONEZ=055,037,03"}
            ]
        }
    
    async def execute(
        self,
        command: str,
        timeout: float = 2.0,
        expect_response: bool = True,
        expected_prefixes: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """
        Выполняет отправку команды контроллеру.
        
        Args:
            command: Текст команды (например, "TIME", "COM 001,010")
            timeout: Таймаут ожидания ответа в секундах
            expect_response: Ожидать ли ответ от устройства
            expected_prefixes: Ожидаемые префиксы строк ответа
            
        Returns:
            Словарь с результатом выполнения
        """
        LOGGER.info(">>> [PLC] execute() called with command: '%s'", command)
        LOGGER.info(">>> [PLC] Timeout: %s, expect_response: %s", timeout, expect_response)
        
        # Валидация команды
        if not command or not command.strip():
            LOGGER.error(">>> [PLC] ERROR: Empty command!")
            return {
                "success": False,
                "error": "Команда не может быть пустой",
                "data": None
            }
        
        command = command.strip()
        LOGGER.info(">>> [PLC] Stripped command: '%s'", command)
        
        # Парсим естественный язык в PLC-команду
        parsed_cmd = self._parse_natural_command(command)
        if parsed_cmd != command:
            LOGGER.info(">>> [PLC] Natural language parsed: '%s' -> '%s'", command, parsed_cmd)
            command = parsed_cmd
        else:
            LOGGER.info(">>> [PLC] Command passed as-is (no parsing needed): '%s'", command)
        
        LOGGER.info(">>> [PLC] Final command to execute: '%s'", command)
        LOGGER.info(">>> [PLC] Executing PLC command: '%s' (expect_response=%s)", command, expect_response)
        
        # Проверяем подключение
        conn_state = self.device.get_connection_state()
        LOGGER.info(">>> [PLC] Device connection state: %s", conn_state)
        
        if not conn_state.get("connected"):
            LOGGER.warning("Device not connected!")
            return {
                "success": False,
                "error": "Нет подключения к контроллеру",
                "data": None
            }
        
        # Обработка команды "выключить всё" - отправляем 0 для всех каналов с задержкой
        if command.upper() == "ВЫКЛЮЧИТЬ ВСЁ":
            LOGGER.info("Executing 'ВЫКЛЮЧИТЬ ВСЁ' - turning off all spectral channels")
            try:
                results = []
                # Каналы: red=140, blue=160, farred=180, white=200
                channels = [
                    (140, "красный"),
                    (160, "синий"),
                    (180, "дальний красный"),
                    (200, "белый")
                ]
                for base, name in channels:
                    cmd = f"COMA 001,{base:03d}"
                    LOGGER.info("Sending: %s for %s", cmd, name)
                    await asyncio.sleep(0.05)
                    await self.device.send_command(cmd, timeout=0.5, expect_response=False)
                    results.append(cmd)
                    await asyncio.sleep(0.05)
                
                LOGGER.info("All channels turned off successfully")
                return {
                    "success": True,
                    "command": command,
                    "response": results,
                    "data": {"type": "spectral_off", "channels": channels}
                }
            except Exception as exc:
                LOGGER.exception("Failed to turn off channels: %s", exc)
                return {
                    "success": False,
                    "error": f"Ошибка выключения: {exc}",
                    "data": None
                }
        
        # Обработка "ВСЕ_СПЕКТРЫ N" - устанавливает все каналы на уровень N%
        if command.upper().startswith("ВСЕ_СПЕКТРЫ"):
            parts = command.split()
            if len(parts) >= 2:
                try:
                    percent = int(parts[1])
                    LOGGER.info("Executing 'ВСЕ_СПЕКТРЫ %d%%'", percent)
                except:
                    percent = 50
            else:
                percent = 50
            
            try:
                results = []
                channels = [
                    (140, "красный"),
                    (160, "синий"),
                    (180, "дальний красный"),
                    (200, "белый")
                ]
                
                # Масштабирование
                if percent <= 0:
                    scaled = 0
                elif percent <= 10:
                    scaled = 1
                else:
                    scaled = (percent // 5) - 1
                scaled = max(0, min(19, scaled))
                
                for base, name in channels:
                    cmd = f"COMA 001,{base + scaled:03d}"
                    LOGGER.info("Sending: %s for %s (level=%d%%)", cmd, name, percent)
                    await asyncio.sleep(0.05)
                    await self.device.send_command(cmd, timeout=0.5, expect_response=False)
                    results.append(cmd)
                    await asyncio.sleep(0.05)
                
                LOGGER.info("All spectral channels set to %d%%", percent)
                return {
                    "success": True,
                    "command": command,
                    "response": results,
                    "data": {"type": "all_spectral", "percent": percent}
                }
            except Exception as exc:
                LOGGER.exception("Failed to set spectral channels: %s", exc)
                return {
                    "success": False,
                    "error": f"Ошибка: {exc}",
                    "data": None
                }
        
        try:
            prefixes = tuple(expected_prefixes) if expected_prefixes else ()
            cmd_upper = command.upper()

            # СЦЕНА - активация сцены
            if cmd_upper.startswith("СЦЕНА"):
                scene_match = re.search(r'СЦЕНА\s*(\d+)', cmd_upper)
                if scene_match:
                    scene_no = int(scene_match.group(1))
                    scene_no = max(1, min(20, scene_no))
                    LOGGER.info("Executing scene activation: %d", scene_no)
                    if self.device.test_mode:
                        LOGGER.info("TEST MODE: Would send COMA 001,%03d", 10 + scene_no)
                        return {
                            "success": True,
                            "command": command,
                            "response": [f"[TEST] СЦЕНА {scene_no} activated"],
                            "data": {"type": "scene_activate", "scene": scene_no, "test": True}
                        }
                    address = "001"
                    code = 10 + scene_no
                    coma_cmd = f"COMA{address},{code:03d}"
                    LOGGER.info("Sending COMA command: %s", coma_cmd)
                    await asyncio.sleep(0.05)
                    lines = await self.device.send_command(
                        command=coma_cmd,
                        expected_prefixes=(),
                        timeout=0.35,
                        max_lines=32,
                        expect_response=False
                    )
                    LOGGER.info("Scene activation command sent")
                    return {
                        "success": True,
                        "command": coma_cmd,
                        "scene": scene_no,
                        "response": lines,
                        "data": {
                            "type": "scene_activate",
                            "scene": scene_no,
                            "address": address,
                            "code": code
                        },
                        "raw_lines": lines
                    }
                return {
                    "success": False,
                    "error": "Не удалось определить номер сцены",
                    "data": None
                }
            
            if cmd_upper.startswith(("COM ", "COMA", "ЯРКОСТЬ")):
                prefixes = ()
                expect_response = False
            
            # Для этих команд пропускаем test_mode check и сразу отправляем
            if self.device.test_mode and not cmd_upper.startswith(("COM ", "COMA", "ЯРКОСТЬ")):
                LOGGER.info("TEST MODE: Would send command: '%s'", command)
                await asyncio.sleep(0.1)
                return {
                    "success": True,
                    "command": command,
                    "response": [f"[TEST] {command}"],
                    "data": {"type": "test", "test": True, "command": command}
                }
            
            lines = await self.device.send_command(
                command=command,
                expected_prefixes=prefixes,
                timeout=timeout,
                max_lines=260,
                expect_response=expect_response
            )
            LOGGER.info("PLC response received: %d lines", len(lines))
            if lines:
                LOGGER.debug("First response line: %s", lines[0] if lines else "")
            parsed_data = self._parse_response(command, lines)
            LOGGER.info("Command executed successfully")
            return {
                "success": True,
                "command": command,
                "response": lines,
                "data": parsed_data,
                "raw_lines": lines
            }
        except TimeoutError as exc:
            LOGGER.warning("PLC command timeout: %s", exc)
            return {
                "success": False,
                "error": f"Таймаут: {exc}",
                "command": command,
                "data": None
            }
        except Exception as exc:
            LOGGER.exception("PLC command failed: %s", exc)
            return {
                "success": False,
                "error": str(exc),
                "command": command,
                "data": None
            }
    
    def _parse_response(self, command: str, lines: list[str]) -> dict[str, Any]:
        """
        Парсит ответ контроллера в структурированный вид.
        
        Args:
            command: Отправленная команда
            lines: Строки ответа
            
        Returns:
            Словарь с распарсенными данными
        """
        if not lines:
            return {"empty": True}
        
        command_upper = command.upper()
        
        # TIME
        if command_upper.startswith("TIME"):
            return self._parse_time(lines)
        
        # GEONEZ
        if command_upper.startswith("GEONEZ"):
            return self._parse_geo(lines)
        
        # KEYS
        if command_upper.startswith("KEYS"):
            return self._parse_bits(lines, "KEYS")
        
        # MASK
        if command_upper.startswith("MASK"):
            return self._parse_bits(lines, "MASK")
        
        # SHED
        if command_upper.startswith("SHED"):
            return self._parse_schedule(lines)
        
        # COM / COMA - просто возвращаем строки
        return {
            "lines": lines,
            "line_count": len(lines)
        }

    def _parse_natural_command(self, command: str) -> str:
        """Парсит естественный язык в команду PLC."""
        cmd_lower = command.lower().strip()

        # Яркость: "включи свет", "яркость 5", "свет на 50%", "выключи"
        brightness_match = re.search(r'яркост[ья]?\s*(\d+)', cmd_lower)
        if brightness_match:
            level = int(brightness_match.group(1))
            level = max(0, min(10, level))  # Ограничиваем 0-10
            return f"ЯРКОСТЬ {level}"
        
        if re.search(r'выключи\s*(свет|все)?', cmd_lower):
            return "ВЫКЛЮЧИТЬ ВСЁ"  # Специальная команда для выключения спектров
        
        if re.search(r'включи\s*(свет|все)?', cmd_lower) or cmd_lower in ['включи', 'включить', 'полный свет']:
            return "ЯРКОСТЬ 10"
        
        # Сцена: "запусти сцену 5", "сцена 3", "активируй сценарий 2"
        scene_match = re.search(r'(?:сцен[ау]|сценарий)\s*(\d+)', cmd_lower)
        if scene_match:
            scene = int(scene_match.group(1))
            scene = max(1, min(20, scene))  # Ограничиваем 1-20
            return f"СЦЕНА {scene}"
        
        if re.search(r'запусти\s*сцен', cmd_lower) or re.search(r'активируй\s*сцен', cmd_lower):
            if scene_match:
                return f"СЦЕНА {int(scene_match.group(1))}"
        
        # Время: "прочитай время", "который час", "время"
        if re.search(r'(?:прочитай|читай|покажи)\s*(время|час)', cmd_lower) or \
           cmd_lower in ['время', 'который час', 'время?']:
            return "ВРЕМЯ"
        
        # Ключи: "прочитай ключи", "keys", "какие ключи"
        if re.search(r'(?:прочитай|читай)\s*(ключ|keys)', cmd_lower) or \
           cmd_lower in ['ключи', 'keys', 'какие ключи']:
            return "КЛЮЧ"
        
        # Маска: "прочитай маску", "mask"
        if re.search(r'(?:прочитай|читай)\s*маск', cmd_lower) or \
           cmd_lower in ['маска', 'mask']:
            return "МАСКА"
        
        # Геолокация: "прочитай гео", "координаты"
        if re.search(r'(?:прочитай|читай)\s*гео', cmd_lower) or \
           cmd_lower in ['гео', 'координаты', 'геолокация']:
            return "ГЕО"
        
        # Расписание: "прочитай расписание"
        if re.search(r'(?:прочитай|читай)\s*расписани', cmd_lower) or \
           cmd_lower in ['расписание', 'расписание?']:
            return "РАСПИСАНИЕ"
        
        # Все спектры: "все спектры 50%", "все каналы 30%", "спектры максимум"
        all_spectral_match = re.search(r'(?:все\s*)?(?:спектр|канал)[а-я]?\s*(?:на\s*)?(\d+)%?', cmd_lower)
        if all_spectral_match and re.search(r'все\s*(?:спектр|канал)', cmd_lower):
            level = int(all_spectral_match.group(1))
            return f"ВСЕ_СПЕКТРЫ {level}"
        
        # Максимум/минимум для спектров
        if re.search(r'спектр(?:ы|а)?\s*(?:максимум|макс|полный)', cmd_lower):
            return "ВСЕ_СПЕКТРЫ 100"
        
        if re.search(r'спектр(?:ы|а)?\s*(?:минимум|выключи)', cmd_lower) or \
           re.search(r'выключи\s*(?:все|спектр|канал)', cmd_lower):
            return "ВЫКЛЮЧИТЬ ВСЁ"
        
        # Спектральные каналы: "красный 50", "синий 30%", "белый на полную"
        spectral = self._parse_spectral_command(cmd_lower)
        if spectral:
            return spectral
        
        # Если команда уже похожа на PLC-команду, возвращаем как есть
        if re.match(r'^(?:время|ключ|маска|гео|расписани|яркость|ком[а]?|сцен)\s*[,=]?\s*\d?', 
                   cmd_lower) or \
           re.match(r'^кома\s*\d{3},\d{3}', cmd_lower) or \
           re.match(r'^ком\s*\d{3},\d{3}', cmd_lower):
            return command.upper()
        
        LOGGER.warning("Could not parse natural command: %s", command)
        return command
    
    def _parse_spectral_command(self, cmd_lower: str) -> Optional[str]:
        """Парсит команды управления спектральными каналами.
        
        Формат COMA: COMA AAA,BCC
        Где B = базовый код канала (14=red, 16=blue, 18=farred, 20=white)
        CC = значение 0-19
        """
        # Все спектры сразу: "все спектры 50%", "все каналы 30%"
        all_match = re.search(r'(?:все\s*)?(?:спектр|канал)[а-я]?\s*(?:на\s*)?(\d+)%?', cmd_lower)
        if all_match and re.search(r'все\s*(?:спектр|канал)', cmd_lower):
            level = int(all_match.group(1))
            return f"ВСЕ_СПЕКТРЫ {level}"
        
        # Красный канал: "красный 50", "красный 50%", "красный на 128"
        red_match = re.search(r'красн(?:ый|ого|ую)?\s*(?:канал(?:а|у|ом))?\s*(?:на\s*)?(\d+)%?', cmd_lower)
        if red_match:
            return self._build_spectral_command("red", int(red_match.group(1)))
        
        # Синий канал
        blue_match = re.search(r'син(?:ий|его|юю)?\s*(?:канал(?:а|у|ом))?\s*(?:на\s*)?(\d+)%?', cmd_lower)
        if blue_match:
            return self._build_spectral_command("blue", int(blue_match.group(1)))
        
        # Белый канал
        white_match = re.search(r'бел(?:ый|ого|ую)?\s*(?:канал(?:а|у|ом))?\s*(?:на\s*)?(\d+)%?', cmd_lower)
        if white_match:
            return self._build_spectral_command("white", int(white_match.group(1)))
        
        # Дальний красный
        far_red_match = re.search(r'дальн(?:ий|его)?\s*(?:красн(?:ый|ого))?\s*(?:на\s*)?(\d+)%?', cmd_lower)
        if far_red_match:
            return self._build_spectral_command("farred", int(far_red_match.group(1)))
        
        return None
    
    def _build_spectral_command(self, channel: str, level: int) -> str:
        """Строит команду COMA для спектрального канала.
        
        Масштабирование процента в код:
        - 0% → 0
        - 1-10% → 1
        - 11-100% → (percent // 5) - 1 (дает 0-19)
        """
        # Базовые коды каналов
        base_codes = {
            "red": 140,
            "blue": 160,
            "farred": 180,
            "white": 200
        }
        
        base = base_codes.get(channel.lower(), 0)
        
        # Масштабирование
        if level <= 0:
            scaled = 0
        elif level <= 10:
            scaled = 1
        else:
            scaled = (level // 5) - 1
        
        # Ограничиваем 0-19
        scaled = max(0, min(19, scaled))
        
        return f"COMA 001,{base + scaled:03d}"
    
    def _parse_spectral_level_to_percent(self, level: int) -> int:
        """Конвертирует значение 0-255 в проценты для ответа."""
        if level == 0:
            return 0
        return (level * 100) // 255
    
    def _parse_time(self, lines: list[str]) -> dict[str, Any]:
        """Парсит ответ TIME."""
        time_pattern = re.compile(
            r"TIME[=\s](?P<time>\d{2}:\d{2}:\d{2})\s+DAY[=\s]?(?P<day>\d)\s+DATE[=\s]?(?P<date>\d{2}\.\d{2}\.\d{2})",
            re.IGNORECASE
        )
        
        for line in lines:
            match = time_pattern.search(line)
            if match:
                return {
                    "type": "time",
                    "time": match.group("time"),
                    "day": int(match.group("day")),
                    "date": match.group("date"),
                    "raw": line
                }
        
        return {"type": "time", "error": "Не удалось разобрать ответ", "lines": lines}
    
    def _parse_geo(self, lines: list[str]) -> dict[str, Any]:
        """Парсит ответ GEONEZ."""
        geo_pattern = re.compile(
            r"Lat=(?P<lat>\d{3})\s+Lon=(?P<lon>\d{3})\s+Zone=\s*(?P<zone>\d{1,2})",
            re.IGNORECASE
        )
        
        for line in lines:
            match = geo_pattern.search(line)
            if match:
                return {
                    "type": "geo",
                    "lat": int(match.group("lat")),
                    "lon": int(match.group("lon")),
                    "zone": int(match.group("zone")),
                    "raw": line
                }
        
        return {"type": "geo", "error": "Не удалось разобрать ответ", "lines": lines}
    
    def _parse_bits(self, lines: list[str], kind: str) -> dict[str, Any]:
        """Парсит ответ KEYS/MASK."""
        bits_pattern = re.compile(rf"^(?P<kind>{kind})=(?P<bits>[01]{{3}})$", re.IGNORECASE)
        
        for line in lines:
            match = bits_pattern.match(line.strip())
            if match:
                bits = match.group("bits")
                return {
                    "type": kind.lower(),
                    "raw": bits,
                    "a": bits[0] == "1",
                    "b": bits[1] == "1",
                    "c": bits[2] == "1",
                    "bits": bits
                }
        
        return {"type": kind.lower(), "error": "Не удалось разобрать ответ", "lines": lines}
    
    def _parse_schedule(self, lines: list[str]) -> dict[str, Any]:
        """Парсит ответ SHED."""
        schedule_pattern = re.compile(
            r"^(?P<index>\d{2})\s+(?P<active>[01])\s+(?P<days>[01]{7})\s+"
            r"(?:"
            r"(?P<time_type_compact>[0-2])(?P<sign_compact>[+-])(?P<hours_compact>\d{2}):(?P<minutes_compact>\d{2})"
            r"|"
            r"(?P<time_type_split>[0-2])\s+(?P<hours_split>\d{2}):(?P<minutes_split>\d{2})"
            r")\s+"
            r"(?P<address>\d{3})\s+(?P<command>\d{3})(?:\s+(?P<level>\d{3,4}))?$"
        )
        
        entries = []
        for line in lines:
            match = schedule_pattern.match(line.strip())
            if match:
                # Определяем формат времени
                if match.group("time_type_compact") is not None:
                    time_type = int(match.group("time_type_compact"))
                    sign = match.group("sign_compact") or "+"
                    hours = match.group("hours_compact")
                    minutes = match.group("minutes_compact")
                else:
                    time_type = int(match.group("time_type_split"))
                    sign = "+"
                    hours = match.group("hours_split")
                    minutes = match.group("minutes_split")
                
                level_raw = match.group("level")
                entries.append({
                    "index": int(match.group("index")),
                    "active": match.group("active") == "1",
                    "days": [day == "1" for day in match.group("days")],
                    "time_type": time_type,
                    "sign": sign,
                    "time": f"{hours}:{minutes}",
                    "address": int(match.group("address")),
                    "command": int(match.group("command")),
                    "level": int(level_raw) if level_raw is not None else 0,
                    "raw": line
                })
        
        return {
            "type": "schedule",
            "count": len(entries),
            "entries": entries
        }


# Регистрируем инструмент
Tool = PlcCommandTool
