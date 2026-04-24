"""
Scene Control Tool - инструмент для управления сценариями и спектральными каналами.
Реализует высокоуровневые операции для записи/воспроизведения сцен.
"""
from __future__ import annotations

import asyncio
from typing import Any, Optional

from backend.device import DeviceService

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import Tool


class SceneControlTool(Tool):
    """
    Инструмент для управления сценариями PLC-контроллера.
    
    Операции:
    - Активация сценария
    - Запись сценария (с предварительной установкой каналов)
    - Установка спектральных каналов
    - Установка стартового сценария
    """
    
    # Маппинг названий каналов в коды
    CHANNEL_CODES = {
        "red": 140,
        "красный": 140,
        "blue": 160,
        "синий": 160,
        "farred": 180,
        "far-red": 180,
        "дальний": 180,
        "дальний красный": 180,
        "white": 200,
        "белый": 200,
    }
    
    def __init__(self, device: DeviceService) -> None:
        super().__init__(device, name="scene_control")
    
    def get_schema(self) -> dict[str, Any]:
        """Возвращает схему параметров инструмента."""
        return {
            "name": self.name,
            "description": "Управление сценариями и спектральными каналами PLC",
            "parameters": {
                "action": {
                    "type": "string",
                    "description": "Действие: activate, save, set_channel, set_start",
                    "required": True,
                    "enum": ["activate", "save", "set_channel", "set_start"]
                },
                "scene": {
                    "type": "number",
                    "description": "Номер сцены (1-20)",
                    "min": 1,
                    "max": 20
                },
                "channel": {
                    "type": "string",
                    "description": "Канал: red, blue, farred, white",
                    "enum": ["red", "blue", "farred", "white"]
                },
                "percent": {
                    "type": "number",
                    "description": "Мощность канала в процентах (0-100)",
                    "min": 0,
                    "max": 100
                },
                "address": {
                    "type": "number",
                    "description": "Адрес устройства (AI или AG)",
                    "default": 0
                },
                "address_type": {
                    "type": "string",
                    "description": "Тип адреса: ai (индивидуальный) или ag (групповой)",
                    "enum": ["ai", "ag"],
                    "default": "ag"
                },
                "channels": {
                    "type": "object",
                    "description": "Объект с мощностями каналов для записи сцены",
                    "properties": {
                        "red": {"type": "number", "min": 0, "max": 100},
                        "blue": {"type": "number", "min": 0, "max": 100},
                        "farred": {"type": "number", "min": 0, "max": 100},
                        "white": {"type": "number", "min": 0, "max": 100}
                    }
                }
            },
            "examples": [
                {"action": "activate", "scene": 5},
                {"action": "save", "scene": 3, "channels": {"red": 50, "blue": 30, "white": 80}},
                {"action": "set_channel", "channel": "red", "percent": 75},
                {"action": "set_start", "scene": 1}
            ]
        }
    
    async def execute(
        self,
        action: str,
        scene: Optional[int] = None,
        channel: Optional[str] = None,
        percent: Optional[int] = None,
        address: int = 0,
        address_type: str = "ag",
        channels: Optional[dict[str, int]] = None,
        timeout: float = 0.5
    ) -> dict[str, Any]:
        """
        Выполняет действие над сценарием.
        
        Args:
            action: Тип действия (activate/save/set_channel/set_start)
            scene: Номер сцены (1-20)
            channel: Название канала (red/blue/farred/white)
            percent: Мощность канала в процентах (0-100)
            address: Адрес устройства
            address_type: Тип адреса (ai/ag)
            channels: Словарь каналов для записи сцены
            timeout: Таймаут для команд
            
        Returns:
            Словарь с результатом выполнения
        """
        # Проверяем подключение
        if not self.device.get_connection_state()["connected"]:
            return {
                "success": False,
                "error": "Нет подключения к контроллеру",
                "data": None
            }
        
        # Вычисляем адрес для команд
        if address_type == "ag":
            if address == 0:
                addr_code = 0
            else:
                addr_code = 220 + address
        else:  # ai
            addr_code = address
        
        addr_str = f"{addr_code:03d}"
        
        try:
            if action == "activate":
                return await self._activate_scene(addr_str, scene, timeout)
            
            elif action == "save":
                return await self._save_scene(addr_str, scene, channels, timeout)
            
            elif action == "set_channel":
                return await self._set_channel(addr_str, channel, percent, timeout)
            
            elif action == "set_start":
                return await self._set_start(addr_str, timeout)
            
            else:
                return {
                    "success": False,
                    "error": f"Неизвестное действие: {action}",
                    "data": None
                }
                
        except Exception as exc:
            return {
                "success": False,
                "error": str(exc),
                "data": None
            }
    
    async def _activate_scene(
        self,
        addr: str,
        scene: Optional[int],
        timeout: float
    ) -> dict[str, Any]:
        """Активирует сценарий."""
        if not scene or not (1 <= scene <= 20):
            return {
                "success": False,
                "error": "Сцена должна быть в диапазоне 1-20",
                "data": None
            }
        
        code = 10 + scene
        command = f"COMA{addr},{code:03d}"
        
        lines = await self.device.send_command(
            command=command,
            timeout=timeout,
            expect_response=False
        )
        
        return {
            "success": True,
            "action": "activate",
            "scene": scene,
            "command": command,
            "response": lines
        }
    
    async def _save_scene(
        self,
        addr: str,
        scene: Optional[int],
        channels: Optional[dict[str, int]],
        timeout: float
    ) -> dict[str, Any]:
        """
        Записывает сценарий с указанными каналами.
        
        Последовательность:
        1. COMA AAA,220 - вход в режим записи
        2. COMA AAA,14x - Красный
        3. COMA AAA,16x - Синий
        4. COMA AAA,18x - Дальний красный
        5. COMA AAA,20x - Белый
        6. COMA AAA,03N - запись сцены N
        """
        if not scene or not (1 <= scene <= 20):
            return {
                "success": False,
                "error": "Сцена должна быть в диапазоне 1-20",
                "data": None
            }
        
        if not channels:
            return {
                "success": False,
                "error": "Не указаны каналы для записи",
                "data": None
            }
        
        result_lines = []
        
        # 1. Вход в режим записи
        command_start = f"COMA{addr},220"
        await self.device.send_command(command_start, timeout=timeout, expect_response=False)
        await asyncio.sleep(0.5)  # Пауза после входа в режим
        
        # 2-5. Установка каналов в порядке PLT_1
        channel_order = ["red", "blue", "farred", "white"]
        
        for ch_name in channel_order:
            ch_percent = channels.get(ch_name, 0)
            ch_code = self._calc_channel_code(ch_name, ch_percent)
            
            if ch_code is not None:
                command = f"COMA{addr},{ch_code:03d}"
                await self.device.send_command(command, timeout=timeout, expect_response=False)
                await asyncio.sleep(0.15)  # Пауза между каналами
        
        # 6. Запись сцены
        await asyncio.sleep(0.3)  # Пауза перед записью
        save_code = 30 + scene
        command_save = f"COMA{addr},{save_code:03d}"
        lines = await self.device.send_command(command_save, timeout=timeout, expect_response=False)
        
        return {
            "success": True,
            "action": "save",
            "scene": scene,
            "channels": channels,
            "command": command_save,
            "response": lines
        }
    
    async def _set_channel(
        self,
        addr: str,
        channel: Optional[str],
        percent: Optional[int],
        timeout: float
    ) -> dict[str, Any]:
        """Устанавливает мощность спектрального канала."""
        if not channel:
            return {
                "success": False,
                "error": "Не указан канал",
                "data": None
            }
        
        if percent is None:
            return {
                "success": False,
                "error": "Не указана мощность канала",
                "data": None
            }
        
        ch_code = self._calc_channel_code(channel, percent)
        
        if ch_code is None:
            return {
                "success": False,
                "error": f"Неизвестный канал: {channel}",
                "data": None
            }
        
        command = f"COMA{addr},{ch_code:03d}"
        lines = await self.device.send_command(command, timeout=timeout, expect_response=False)
        
        return {
            "success": True,
            "action": "set_channel",
            "channel": channel,
            "percent": percent,
            "code": ch_code,
            "command": command,
            "response": lines
        }
    
    async def _set_start(
        self,
        addr: str,
        timeout: float
    ) -> dict[str, Any]:
        """Устанавливает стартовый сценарий."""
        command = f"COMA{addr},220"
        lines = await self.device.send_command(command, timeout=timeout, expect_response=False)
        
        return {
            "success": True,
            "action": "set_start",
            "command": command,
            "response": lines
        }
    
    def _calc_channel_code(self, channel: str, percent: int) -> Optional[int]:
        """
        Вычисляет код команды для канала.
        
        Масштабирование:
        - 0% → 0
        - 1-10% → 1
        - 11-100% → (percent // 5) - 1
        
        Базовые коды:
        - red: 140
        - blue: 160
        - farred: 180
        - white: 200
        """
        # Нормализация названия канала
        ch_lower = channel.lower().strip().replace("-", " ").replace("_", " ")
        
        base_code = self.CHANNEL_CODES.get(ch_lower)
        if base_code is None:
            return None
        
        # Масштабирование процента
        if percent <= 0:
            scaled = 0
        elif percent <= 10:
            scaled = 1
        else:
            scaled = (percent // 5) - 1
        
        # Ограничиваем диапазон 0-19
        scaled = max(0, min(19, scaled))
        
        return base_code + scaled
