"""
PLC Nova AI Agent - основной модуль управления агентом.
Интегрирует skills, tools, LM Studio API и голосовой ввод.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import sys
import wave
from pathlib import Path
from typing import Any, Callable, Coroutine, Optional, Dict, List
from dataclasses import dataclass, field

APP_DIR = Path(__file__).resolve().parent
IS_FROZEN = "__compiled__" in globals()

if IS_FROZEN:
    PROJECT_DIR = Path(sys.argv[0]).resolve().parent
else:
    PROJECT_DIR = APP_DIR.parent

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.device import DeviceService, list_available_ports

# Logger
LOGGER = logging.getLogger("plc_nova.agent")
LOGGER.setLevel(logging.DEBUG)
if not LOGGER.handlers:
    root = logging.getLogger("plc_nova")
    if root.handlers:
        for h in root.handlers:
            LOGGER.addHandler(h)
        # Отключаем propagate чтобы избежать дублирования
        LOGGER.propagate = False

AGENT_DIR = PROJECT_DIR / "agent"
SKILLS_DIR = AGENT_DIR / "skills"
TOOLS_DIR = AGENT_DIR / "tools"

LM_STUDIO_API_CONFIG = {
    "base_url": "http://127.0.0.1:1234",
    "api_token": "",
    "model": "",
    "temperature": 0.7,
    "max_tokens": 512,
    "context_length": 4096,
}

DEFAULT_MODEL_CONFIG = {
    "model_key": None,
    "instance_id": None,
    "context_size": 4096,
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "repeat_penalty": 1.1,
    "reasoning_enabled": False
}

DEFAULT_SPEECH_CONFIG = {
    "language": "ru-RU",
    "energy_threshold": 4000,
    "pause_threshold": 0.8,
}


class PLCAgent:
    def __init__(self, device: Optional[DeviceService] = None) -> None:
        print("[AGENT] PLCAgent starting...")
        LOGGER.info("=== PLCAgent.__init__() ===")
        self.device = device if device is not None else DeviceService()
        self._skills: dict[str, "Skill"] = {}
        self._tools: dict[str, "Tool"] = {}
        self._models_available = False
        self._speech_available = False
        self._lm_studio_available = False
        self._model_config = DEFAULT_MODEL_CONFIG.copy()
        self._speech_config = DEFAULT_SPEECH_CONFIG.copy()
        self._chat_history: List[Dict[str, str]] = []
        self._mic_enabled = False
        self._current_model_key = None
        self.test_mode = False
        self.device.test_mode = False

        # Проверяем LM Studio
        print("[AGENT] Checking LM Studio...")
        lm_ok = self.check_lm_studio()
        print(f"[AGENT] LM Studio check: {lm_ok}")
        
        # Обновляем список моделей и текущую модель
        print("[AGENT] Fetching model list and current model...")
        model_files = self.list_model_files()
        print(f"[AGENT] Found {len(model_files)} models")
        
        # Пытаемся получить текущую модель
        current = self.get_current_model()
        if current:
            self._current_model_key = current
            print(f"[AGENT] Current model: {current}")

        # Проверяем модели
        print("[AGENT] Checking models...")
        models_ok = self.check_models()
        print(f"[AGENT] Models check: {models_ok}")
        
        # Обновляем список моделей
        print("[AGENT] Fetching model list...")
        model_files = self.list_model_files()
        print(f"[AGENT] Found {len(model_files)} models: {model_files}")

        # Проверяем speech
        print("[AGENT] Checking Speech...")
        speech_ok = self.check_speech()
        print(f"[AGENT] Speech check: {speech_ok}")

        print("[AGENT] Init complete")

    def check_lm_studio(self) -> bool:
        print("[AGENT] check_lm_studio() calling LM Studio API...")
        LOGGER.info("=== check_lm_studio() ===")
        try:
            import requests
            base_url = LM_STUDIO_API_CONFIG["base_url"]
            headers = {"Content-Type": "application/json"}
            print(f"[AGENT] Calling: {base_url}/api/v1/models")
            response = requests.get(f"{base_url}/api/v1/models", headers=headers, timeout=5)
            print(f"[AGENT] LM Studio response: {response.status_code}")
            LOGGER.info("LM Studio response: %d", response.status_code)
            if response.status_code == 200:
                self._lm_studio_available = True
                print("[AGENT] LM Studio AVAILABLE")
                return True
            self._lm_studio_available = False
            print(f"[AGENT] LM Studio error: {response.status_code}")
            return False
        except Exception as exc:
            print(f"[AGENT] LM Studio exception: {exc}")
            LOGGER.error("LM Studio error: %s", exc)
            self._lm_studio_available = False
            return False

    def check_models(self) -> bool:
        # Обновляем _models_available на основе LM Studio
        self._models_available = self._lm_studio_available
        return self._lm_studio_available

    def get_current_model(self) -> Optional[str]:
        print("[AGENT] get_current_model() called")
        try:
            import requests
            base_url = LM_STUDIO_API_CONFIG["base_url"]
            headers = {"Content-Type": "application/json"}
            response = requests.get(f"{base_url}/api/v1/models", headers=headers, timeout=5)
            print(f"[AGENT] /api/v1/models response: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                print(f"[AGENT] Found {len(models)} models")
                for model in models:
                    print(f"[AGENT] Model: {model.get('key')}, loaded: {model.get('loaded_instances')}")
                    if model.get("loaded_instances"):
                        key = model.get("key")
                        instance_id = model.get("loaded_instances", [{}])[0].get("id")
                        self._current_model_key = key
                        self._model_config["model_key"] = key
                        self._model_config["use_lm_studio"] = True
                        self._model_config["instance_id"] = instance_id
                        print(f"[AGENT] Current model: {key}, instance_id: {instance_id}")
                        return key
        except Exception as exc:
            print(f"[AGENT] get_current_model error: {exc}")
            LOGGER.error("get_current_model error: %s", exc)
        return None

    def list_model_files(self) -> List[str]:
        models = []
        try:
            import requests
            base_url = LM_STUDIO_API_CONFIG["base_url"]
            headers = {"Content-Type": "application/json"}
            response = requests.get(f"{base_url}/api/v1/models", headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                all_models = data.get("models", [])
                loaded_key = None
                for model in all_models:
                    if model.get("loaded_instances"):
                        loaded_key = model.get("key")
                for model in all_models:
                    if model.get("type") == "llm":
                        key = model.get("key", "")
                        display = model.get("display_name", key)
                        if key:
                            if key == loaded_key:
                                models.append(f"{display} ({key}) [ЗАГРУЖЕНА]")
                            else:
                                models.append(f"{display} ({key})")
        except Exception as exc:
            LOGGER.error("Failed to fetch models: %s", exc)
        return models

    def load_model(self, model_key: str, config: Optional[Dict] = None) -> bool:
        cfg = {**self._model_config, **(config or {})}
        if self._lm_studio_available:
            return self._load_lm_studio_model(model_key, cfg)
        return False

    def _load_lm_studio_model(self, model_key: str, config: Dict) -> bool:
        actual_key = model_key
        match = re.search(r'\(([^)]+)\)', model_key)
        if match:
            actual_key = match.group(1)
        LOGGER.info("Loading model: %s", actual_key)
        try:
            import requests
            base_url = LM_STUDIO_API_CONFIG["base_url"]
            payload = {
                "model": actual_key,
                "context_length": config.get("context_size", 4096),
            }
            response = requests.post(f"{base_url}/api/v1/models/load", json=payload, headers={"Content-Type": "application/json"}, timeout=60)
            if response.status_code == 200:
                data = response.json()
                self._model_config["model_key"] = model_key
                self._model_config["use_lm_studio"] = True
                # Сохраняем instance_id из ответа
                instance_id = data.get("instance_id")
                if instance_id:
                    self._model_config["instance_id"] = instance_id
                    self._current_model_key = actual_key
                # Сохраняем параметры конфигурации
                if config.get("reasoning") is not None:
                    self._model_config["reasoning"] = config["reasoning"]
                if config.get("temperature") is not None:
                    self._model_config["temperature"] = config["temperature"]
                if config.get("max_tokens") is not None:
                    self._model_config["max_tokens"] = config["max_tokens"]
                if config.get("context_size") is not None:
                    self._model_config["context_size"] = config["context_size"]
                LOGGER.info("Model loaded: %s", instance_id)
                return True
            return False
        except Exception as exc:
            LOGGER.error("Load error: %s", exc)
            return False

    def unload_model(self) -> None:
        instance_id = self._model_config.get("instance_id")
        if instance_id and self._lm_studio_available:
            try:
                import requests
                base_url = LM_STUDIO_API_CONFIG["base_url"]
                requests.post(f"{base_url}/api/v1/models/unload", json={"instance_id": instance_id}, headers={"Content-Type": "application/json"}, timeout=30)
            except Exception as exc:
                LOGGER.error("Unload error: %s", exc)
        self._model_config["model_key"] = None
        self._model_config["use_lm_studio"] = False
        self._model_config["instance_id"] = None
        self._current_model_key = None
        LOGGER.info("Model unloaded")

    def check_speech(self) -> bool:
        print("[AGENT] check_speech() checking...")
        LOGGER.info("=== check_speech() ===")
        try:
            import speech_recognition as sr
            print("[AGENT] SpeechRecognition module found!")
            LOGGER.info("SpeechRecognition available")
            self._speech_available = True
            return True
        except ImportError as exc:
            print(f"[AGENT] SpeechRecognition NOT installed: {exc}")
            LOGGER.warning("SpeechRecognition NOT installed: %s", exc)
            self._speech_available = False
            return False
        except Exception as exc:
            print(f"[AGENT] SpeechRecognition error: {exc}")
            LOGGER.error("SpeechRecognition error: %s", exc)
            self._speech_available = False
            return False

    def load_tools(self) -> list[str]:
        loaded = []
        if not TOOLS_DIR.exists():
            return loaded
        for tool_file in TOOLS_DIR.glob("*.py"):
            if tool_file.name.startswith("_"):
                continue
            try:
                tool_name = tool_file.stem
                import importlib.util
                spec = importlib.util.spec_from_file_location(tool_name, tool_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for attr_name in dir(module):
                        if attr_name.endswith("Tool"):
                            tool_class = getattr(module, attr_name)
                            if callable(tool_class):
                                tool_instance = tool_class(self.device)
                                self._tools[attr_name] = tool_instance
                                loaded.append(attr_name)
                                LOGGER.info("Loaded tool: %s", attr_name)
            except Exception as exc:
                LOGGER.exception("Failed to load tool %s: %s", tool_file.name, exc)
        return loaded

    def load_skills(self) -> list[str]:
        loaded = []
        if not SKILLS_DIR.exists():
            return loaded
        for skill_file in SKILLS_DIR.glob("*.md"):
            if skill_file.name.startswith("_"):
                continue
            try:
                skill_name = skill_file.stem
                content = skill_file.read_text(encoding="utf-8")
                skill = Skill.from_markdown(content, skill_name, self)
                self._skills[skill_name] = skill
                loaded.append(skill_name)
                LOGGER.info("Loaded skill: %s", skill_name)
            except Exception as exc:
                LOGGER.exception("Failed to load skill %s: %s", skill_file.name, exc)
        return loaded

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())
    
    def _get_tools_schema(self) -> list[dict]:
        """Возвращает schema всех tools для передачи в LM Studio."""
        tools_schema = []
        for tool_name, tool in self._tools.items():
            try:
                schema = tool.get_schema()
                # Обёртка в формат OpenAI tools
                tools_schema.append({
                    "type": "function",
                    "function": schema
                })
            except Exception as exc:
                LOGGER.warning("Tool %s get_schema failed: %s", tool_name, exc)
        LOGGER.info("Tools schema prepared: %s tools", len(tools_schema))
        return tools_schema

    def list_skills(self) -> list[str]:
        return list(self._skills.keys())

    async def execute(self, command: str) -> dict[str, Any]:
        print(f"[AGENT] execute() called: '{command}'")
        LOGGER.info("=== execute() called: '%s' ===", command)
        LOGGER.info(">>> [EXEC] Input command: '%s'", command)
        LOGGER.info(">>> [EXEC] Test mode: %s", self.test_mode)
        LOGGER.info(">>> [EXEC] Device connected: %s", self.device.get_connection_state().get("connected"))
        
        is_control_command = self._is_control_command(command)
        print(f"[AGENT] is_control_command: {is_control_command}")
        LOGGER.info(">>> [EXEC] Is control/PLC command: %s", is_control_command)
        
        if not is_control_command:
            print(f"[AGENT] Chat command (not PLC)")
            LOGGER.info(">>> [EXEC] Routing to CHAT (not PLC command)")
            return {"success": True, "command": command, "response": ["Разговорная команда"], "data": {"type": "chat"}}
        
        # Тестовый режим
        if self.test_mode:
            LOGGER.info(">>> [EXEC] TEST MODE active - parsing command only")
            # Пытаемся получить реальную команду PLC
            parsed_command = command
            for skill in self._skills.values():
                if skill.matches(command):
                    tool = self._tools.get("PlcCommandTool")
                    if tool and hasattr(tool, "_parse_natural_command"):
                        parsed_command = tool._parse_natural_command(command)
                        LOGGER.info(">>> [EXEC] TEST MODE parsed: '%s' -> '%s'", command, parsed_command)
                    break
            
            print(f"[AGENT] TEST MODE: Would execute command: '{command}' -> '{parsed_command}'")
            LOGGER.info("TEST MODE: Command '%s' -> parsed: '%s'", command, parsed_command)
            return {"success": True, "command": command, "response": [f"[TEST] {parsed_command}"], "data": {"test": True, "command": parsed_command}}
        
        # Проверка подключения
        if not self.device.get_connection_state().get("connected"):
            print("[AGENT] No device connection!")
            LOGGER.warning("Device not connected!")
            LOGGER.warning(">>> [EXEC] ERROR: No device connection!")
            return {"success": False, "error": "Нет подключения", "requires_connection": True}
        
        LOGGER.info(">>> [EXEC] Checking skills for command: '%s'", command)
        LOGGER.info(">>> [EXEC] Available skills: %s", list(self._skills.keys()))
        
        # Скиллы
        matched_skill = None
        for skill_name, skill in self._skills.items():
            match_result = skill.matches(command)
            LOGGER.info(">>> [EXEC] Skill '%s' matches: %s", skill_name, match_result)
            if match_result:
                matched_skill = skill
                break
        
        if matched_skill:
            LOGGER.info(">>> [EXEC] Executing skill: %s", matched_skill.name)
            try:
                print(f"[AGENT] Executing skill: {matched_skill.name}")
                LOGGER.info("Executing skill: %s for command: '%s'", matched_skill.name, command)
                result = await matched_skill.execute(command, self)
                print(f"[AGENT] Skill result: {result}")
                LOGGER.info(">>> [EXEC] Skill result: %s", result)
                LOGGER.info("Skill '%s' result: %s", matched_skill.name, result)
                return result
            except Exception as exc:
                LOGGER.exception("Skill error: %s", exc)
                LOGGER.error(">>> [EXEC] Skill execution error: %s", exc)
                return {"success": False, "error": str(exc)}
        
        # PLC команда
        LOGGER.info(">>> [EXEC] No skill matched - executing raw PLC command: '%s'", command)
        print(f"[AGENT] Executing raw PLC command: '{command}'")
        return await self._execute_raw_command(command)

    def _is_control_command(self, command: str) -> bool:
        cmd = command.upper().strip()
        
        # Список ключевых слов команд PLC
        control_keywords = [
            "ВКЛЮЧИ", "ВЫКЛЮЧИ", "УСТАНОВИ", "ЗАПИШИ", "АКТИВИРУЙ",
            "СЦЕНА", "СЦЕНАРИЙ", "ЯРКОСТЬ", "ВКЛ", "ВЫКЛ",
            "ВРЕМЯ", "КЛЮЧ", "МАСКА", "ГЕО", "ГЕОНЕЗ", "РАСПИСАНИЕ"
        ]
        
        # Проверяем входные слова пользователя
        cmd_lower = command.lower()
        if any(p in cmd_lower for p in ["включи", "выключи", "установи", "запиши", "активируй", "сценарий", "яркость", "выполни", "запусти", "первый", "второй"]):
            return True
        
        # Проверяем формат команд протокола
        # COMA AAA,CCC - сценарии и спектр
        if re.match(r'^COMA?\s*\d{3},\d{3}$', cmd):
            return True
        # TIME, TIME=... - время
        if re.match(r'^TIME($|=)', cmd):
            return True
        # GEONEZ, GEONEZ=... - геолокация
        if re.match(r'^GEONEZ($|=)', cmd):
            return True
        # KEYS, KEYS=... - ключи
        if re.match(r'^KEYS($|=)', cmd):
            return True
        # MASK, MASK=... - маска
        if re.match(r'^MASK($|=)', cmd):
            return True
        # SHED, SHED=... - расписание
        if re.match(r'^SHED($|=)', cmd):
            return True
        # ВРЕМЯ (cyrillic)
        if cmd in ["ВРЕМЯ", "ВРЕМЯ=", "КЛЮЧ", "КЛЮЧ=", "МАСКА", "МАСКА=", "ГЕО", "ГЕОНЕЗ", "РАСПИСАНИЕ"]:
            return True
        
        # Ещё ключевые слова для команд
        if any(p in cmd_lower for p in ["выполни", "запусти", "первый", "второй", "третий", "сценарий", "сцену"]):
            return True
        
        return False

    async def _execute_raw_command(self, command: str) -> dict[str, Any]:
        LOGGER.info(">>> [RAW] Starting raw PLC command execution: '%s'", command)
        try:
            LOGGER.info(">>> [RAW] Sending command to device...")
            lines = await self.device.send_command(command, timeout=2.0, expect_response=True)
            LOGGER.info(">>> [RAW] Command sent, received %d lines", len(lines) if lines else 0)
            LOGGER.info(">>> [RAW] Response lines: %s", lines)
            return {"success": True, "command": command, "response": lines, "data": {"lines": lines}}
        except Exception as exc:
            LOGGER.error(">>> [RAW] Command execution failed: %s", exc)
            return {"success": False, "error": str(exc), "command": command}

    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if self._model_config.get("use_lm_studio") and self._lm_studio_available:
            return self._generate_lm_studio(prompt, system_prompt)
        return "LM Studio недоступен."

    def _generate_lm_studio(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        try:
            import requests
            base_url = LM_STUDIO_API_CONFIG["base_url"]
            model_key = self._model_config.get("model_key", "")
            if not model_key:
                return "Модель не выбрана"
            
            match = re.search(r'\(([^)]+)\)', model_key)
            actual_key = match.group(1) if match else model_key
            
            # Получаем tools schema для передачи в LM Studio
            # tools НЕ поддерживаются в LM Studio API - используем парсинг ответа
            tools = None  # Пока отключено - парсим ответ вручную
            
            payload = {
                "model": actual_key,
                "input": prompt,
                "temperature": self._model_config.get("temperature", 0.7),
                "max_output_tokens": self._model_config.get("max_tokens", 512),
            }
            # Отправлять reasoning если он явно задан (включая "off")
            reasoning = self._model_config.get("reasoning")
            print(f"DEBUG: reasoning from config = {reasoning}")
            if reasoning is not None and reasoning != "":
                payload["reasoning"] = reasoning
                print(f"DEBUG: Sending reasoning={reasoning}")
            else:
                print(f"DEBUG: Not sending reasoning (value: {reasoning})")
            if tools:
                payload["tools"] = tools
            if system_prompt:
                payload["system_prompt"] = system_prompt
            
            response = requests.post(f"{base_url}/api/v1/chat", json=payload, headers={"Content-Type": "application/json"}, timeout=60)
            if response.status_code == 200:
                data = response.json()
                LOGGER.info("LM Studio response: %s", data)
                output = data.get("output", [])
                LOGGER.info("Output items: %d", len(output))
                
                # Ищем message в output
                for item in output:
                    item_type = item.get("type")
                    LOGGER.info("  Output item: type=%s", item_type)
                    
                    if item_type == "message":
                        content = item.get("content", "").strip()
                        if content:
                            LOGGER.info("  Message content: %s", content[:200])
                            return content
                    elif item_type == "reasoning":
                        LOGGER.info("  Reasoning: %s", item.get("content", "")[:200])
                
                # Если нет message, проверяем есть ли просто текст в output
                if output:
                    # Пробуем получить текст из любого элемента
                    for item in output:
                        content = item.get("content", "")
                        if content:
                            LOGGER.info("Fallback content: %s", content[:200])
                            return content
                
                LOGGER.warning("No message found in output")
                return ""
        except Exception as exc:
            return f"Ошибка: {exc}"

    def set_test_mode(self, enabled: bool) -> None:
        self.test_mode = enabled
        self.device.test_mode = enabled
        LOGGER.info("Test mode: %s", enabled)

    def clear_chat_history(self) -> None:
        self._chat_history = []
        LOGGER.info("Chat history cleared")

    def get_status(self) -> dict[str, Any]:
        # Обновляем текущую модель (с кэшированием)
        current = self._current_model_key or self.get_current_model()
        if current:
            self._model_config["model_key"] = current
            self._model_config["use_lm_studio"] = True
        
        print(f"[AGENT] get_status: current_model={current}")
        
        return {
            "models_available": self._models_available,
            "speech_available": self._speech_available,
            "lm_studio_available": self._lm_studio_available,
            "vosk_available": self._speech_available,
            "mic_enabled": self._mic_enabled,
            "model_files": self.list_model_files(),
            "current_model": current,
            "model_config": self._model_config,
            "tools": self.list_tools(),
            "skills": self.list_skills(),
            "device": self.device.get_connection_state(),
            "chat_history_length": len(self._chat_history),
        }


class Skill:
    def __init__(self, name: str, description: str, triggers: list[str], agent: "PLCAgent" = None):
        self.name = name
        self.description = description
        self.triggers = triggers
        self.agent = agent

    @classmethod
    def from_markdown(cls, content: str, name: str, agent: "PLCAgent" = None) -> "Skill":
        lines = content.split("\n")
        triggers = []
        description = name
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                break
            if line.startswith("triggers:"):
                for t in lines[i+1:]:
                    if t.strip().startswith("-"):
                        triggers.append(t.strip()[1:].strip())
                    elif t.strip() and not t.strip().startswith("#"):
                        break
            elif line.startswith("description:"):
                description = line.split(":", 1)[1].strip()
        return cls(name, description, triggers, agent)

    def matches(self, command: str) -> bool:
        cmd = command.lower()
        return any(t in cmd for t in self.triggers)

    async def execute(self, command: str, agent: "PLCAgent" = None) -> dict[str, Any]:
        if not agent:
            return {"success": False, "error": "AGent not provided"}
        tool = agent._tools.get("PlcCommandTool")
        if tool:
            try:
                return await tool.execute(command=command)
            except Exception as exc:
                return {"success": False, "error": str(exc)}
        return {"success": False, "error": "No tool available"}


class Tool:
    def __init__(self, device: DeviceService, name: str = "tool") -> None:
        self.device = device
        self.name = name

    async def execute(self, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError("Tool must implement execute()")


def get_agent():
    """Returns singleton agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = PLCAgent()
    return _agent_instance


_agent_instance = None
def initialize_agent():
    """Compatibility shim for external imports expecting initialize_agent."""
    return get_agent()
