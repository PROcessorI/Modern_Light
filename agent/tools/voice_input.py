"""
Voice Input Tool - инструмент для распознавания речи через SpeechRecognition.
Поддерживает распознавание с микрофона через Google API.
"""
from __future__ import annotations

import logging
from typing import Any, Optional, Dict
import threading

from backend.device import DeviceService

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import Tool

LOGGER = logging.getLogger("plc_nova.voice")

# Аудио параметры для SpeechRecognition
DEFAULT_SAMPLE_RATE = 16000


class VoiceInputTool(Tool):
    """
    Инструмент для голосового ввода и распознавания речи.
    
    Возможности:
    - Распознавание из WAV-файла
    - Потоковое распознавание с микрофона
    - Постоянный режим прослушивания
    """
    
    def __init__(self, device: DeviceService) -> None:
        super().__init__(device, name="voice_input")
        self._recording = False
        self._last_transcript = ""
        self._recognizer = None
    
    def get_schema(self) -> dict[str, Any]:
        """Возвращает схему параметров инструмента."""
        return {
            "name": self.name,
            "description": "Распознавание речи через SpeechRecognition (Google API)",
            "parameters": {
                "action": {
                    "type": "string",
                    "description": "Действие: recognize, get_status",
                    "enum": ["recognize", "get_status"]
                },
                "audio_data": {
                    "type": "string",
                    "description": "Base64-encoded WAV данные (для recognize)",
                    "format": "base64"
                },
                "sample_rate": {
                    "type": "number",
                    "description": "Частота дискретизации",
                    "default": 16000
                }
            },
            "examples": [
                {"action": "get_status"},
                {"action": "recognize", "audio_data": "<base64>"}
            ]
        }
    
    async def execute(
        self,
        action: str,
        audio_data: Optional[str] = None,
        sample_rate: int = 16000,
    ) -> dict[str, Any]:
        """
        Выполняет действие распознавания речи.
        
        Args:
            action: Тип действия
            audio_data: Base64-encoded WAV данные
            sample_rate: Частота дискретизации
            
        Returns:
            Словарь с результатом
        """
        if action == "get_status":
            return self._get_status()
        
        elif action == "recognize":
            return self._recognize_from_data(audio_data, sample_rate)
        
        else:
            return {
                "success": False,
                "error": f"Неизвестное действие: {action}",
                "data": None
            }
    
    def _get_status(self) -> dict[str, Any]:
        """Возвращает статус голосового ввода."""
        import speech_recognition as sr
        speech_available = True
        
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                pass
        except OSError:
            speech_available = False
        
        return {
            "success": True,
            "speech_available": speech_available,
            "recording": self._recording,
            "last_transcript": self._last_transcript,
            "sample_rate": DEFAULT_SAMPLE_RATE,
        }
    
    def _recognize_from_data(
        self,
        audio_data: Optional[str],
        sample_rate: int
    ) -> dict[str, Any]:
        """
        Распознаёт речь из Base64-encoded WAV данных через Google Speech API.
        
        Args:
            audio_data: Base64-encoded WAV
            sample_rate: Частота дискретизации
            
        Returns:
            Результат распознавания
        """
        import base64
        import speech_recognition as sr
        
        if not audio_data:
            return {
                "success": False,
                "error": "Аудиоданные не предоставлены",
                "data": None
            }
        
        try:
            # Декодируем Base64
            wav_bytes = base64.b64decode(audio_data)
            
            # Создаём AudioData
            audio = sr.AudioData(wav_bytes, sample_rate, 2)
            
            r = sr.Recognizer()
            
            # Используем Google Speech Recognition
            text = r.recognize_google(audio, language="ru-RU")
            
            self._last_transcript = text
            
            return {
                "success": True,
                "action": "recognize",
                "transcript": text,
                "data": {"text": text}
            }
            
        except sr.UnknownValueError:
            return {
                "success": False,
                "error": "Речь не распознана",
                "data": None
            }
        except sr.RequestError as exc:
            return {
                "success": False,
                "error": f"Ошибка сервиса Google: {exc}",
                "data": None
            }
        except Exception as exc:
            LOGGER.exception("Speech recognition failed: %s", exc)
            return {
                "success": False,
                "error": str(exc),
                "data": None
            }
        
