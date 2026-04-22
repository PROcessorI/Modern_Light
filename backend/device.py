from __future__ import annotations

import asyncio
import logging
import re
import subprocess
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque

try:
    import serial
    from serial import SerialException
    from serial.tools import list_ports
except Exception:
    serial = None
    SerialException = Exception
    list_ports = None

try:
    import winreg
except Exception:
    winreg = None


LOGGER = logging.getLogger("plc_nova.device")


@dataclass
class ConnectionSnapshot:
    connected: bool
    port: str
    baudrate: int

    def to_dict(self) -> dict[str, object]:
        """Возвращает состояние подключения в JSON-совместимом виде."""
        return {
            "connected": self.connected,
            "port": self.port,
            "baudrate": self.baudrate,
        }


class DeviceService:
    def __init__(self) -> None:
        """Инициализирует сервис обмена с устройством по реальному COM-порту."""
        self._serial = None
        self._port = ""
        self._baudrate = 9600
        self._lock = asyncio.Lock()
        self._history: Deque[dict[str, str]] = deque(maxlen=800)
        self._last_tx_monotonic = 0.0
        self._last_tx_command = ""
        self._tx_sequence = 0

    # === Transmit pacing / low-level query ===
    # Device controllers require gaps between certain command types (COMA/COM)
    # to process and avoid state glitches. The helpers below centralize the
    # required inter-command gap policy and the synchronous query implementation.

    def get_connection_state(self) -> dict[str, object]:
        """Читает текущее состояние подключения для отображения в UI."""
        connected = bool(self._serial and self._serial.is_open)
        snapshot = ConnectionSnapshot(
            connected=connected,
            port=self._port,
            baudrate=self._baudrate,
        )
        return snapshot.to_dict()

    def get_logs(self, limit: int = 200) -> list[dict[str, str]]:
        """Возвращает последние записи журнала обмена с ограничением по количеству."""
        if limit < 1:
            return []
        return list(self._history)[-limit:]

    async def connect(self, port: str, baudrate: int) -> dict[str, object]:
        """Подключается к указанному COM-порту."""
        if not port:
            raise ValueError("Не указан COM-порт")
        if baudrate <= 0:
            raise ValueError("Скорость baudrate должна быть положительной")

        async with self._lock:
            await asyncio.to_thread(self._connect_sync, port, baudrate)
            return self.get_connection_state()

    async def disconnect(self) -> dict[str, object]:
        """Отключает активное COM-соединение и возвращает актуальный статус."""
        async with self._lock:
            await asyncio.to_thread(self._disconnect_sync)
            return self.get_connection_state()

    async def send_command(
        self,
        command: str,
        expected_prefixes: tuple[str, ...] = (),
        timeout: float = 2.0,
        max_lines: int = 120,
        expect_response: bool = True,
    ) -> list[str]:
        """Отправляет команду устройству и возвращает строки ответа."""
        cleaned = command.strip()
        if not cleaned:
            raise ValueError("Команда не может быть пустой")

        async with self._lock:
            if not self._serial or not self._serial.is_open:
                raise RuntimeError("Последовательный порт не подключен. Сначала выполните подключение.")

            return await asyncio.to_thread(
                self._query_sync,
                cleaned,
                expected_prefixes,
                timeout,
                max_lines,
                expect_response,
            )

    def _connect_sync(self, port: str, baudrate: int) -> None:
        """Синхронно открывает serial-порт с заданными параметрами."""
        if serial is None:
            raise RuntimeError("Пакет pyserial не установлен. Установите зависимости.")

        self._disconnect_sync()
        try:
            LOGGER.info("Opening serial port: %s @ %s", port, baudrate)
            self._serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=0.12,
                write_timeout=2.5,  # Увеличено с 1.0 до 2.5 для надёжной отправки COMA
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False,
            )
        except SerialException as exc:
            LOGGER.exception("Failed to open serial port %s @ %s: %s", port, baudrate, exc)
            raise RuntimeError(f"Не удалось открыть {port}: {exc}") from exc

        self._port = port
        self._baudrate = baudrate
        self._log("sys", f"Подключено: {port} @ {baudrate}")

    def _disconnect_sync(self) -> None:
        """Синхронно закрывает serial-порт, если соединение активно."""
        if self._serial and self._serial.is_open:
            LOGGER.info("Closing serial port: %s", self._port)
            self._serial.close()
            self._log("sys", f"Отключено: {self._port}")
        self._serial = None
        self._last_tx_monotonic = 0.0
        self._last_tx_command = ""
        self._tx_sequence = 0

    def _query_sync(
        self,
        command: str,
        expected_prefixes: tuple[str, ...],
        timeout: float,
        max_lines: int,
        expect_response: bool,
    ) -> list[str]:
        """Синхронно отправляет команду в порт и считывает ответ до таймаута."""
        prefixes = tuple(prefix for prefix in expected_prefixes if prefix)
        if self._serial is None:
            raise RuntimeError("Serial не инициализирован")

        ser = self._serial

        self._tx_sequence += 1
        previous_command = self._last_tx_command or "-"
        # Явный вывод в консоль всех отправляемых команд с последней текущей командой.
        print(
            f"Sending command #{self._tx_sequence}: {command} | previous: {previous_command}",
            flush=True,
        )
        self._log("tx", command)
        payload = (command + "\r\n").encode("ascii", errors="ignore")

        try:
            ser.reset_input_buffer()
            ser.write(payload)
            ser.flush()
            self._last_tx_monotonic = time.monotonic()
            self._last_tx_command = command
            LOGGER.info("TX_RAW: %r", payload)
        except SerialException as exc:
            LOGGER.exception("Serial write failed for command '%s': %s", command, exc)
            raise RuntimeError(f"Ошибка записи в COM-порт: {exc}") from exc

        lines: list[str] = []
        line_buffer = bytearray()
        deadline = time.monotonic() + max(timeout, 0.3)

        while time.monotonic() < deadline and len(lines) < max_lines:
            waiting = getattr(ser, "in_waiting", 0)
            read_size = waiting if isinstance(waiting, int) and waiting > 0 else 1

            try:
                raw = ser.read(read_size)
            except SerialException as exc:
                LOGGER.exception("Serial read failed for command '%s': %s", command, exc)
                raise RuntimeError(f"Ошибка чтения COM-порта: {exc}") from exc

            if not raw:
                continue

            for byte in raw:
                if byte in (10, 13):
                    if line_buffer:
                        line = line_buffer.decode("cp1251", errors="ignore").strip()
                        line_buffer.clear()
                        if line:
                            lines.append(line)
                            self._log("rx", line)
                            if prefixes and any(line.startswith(prefix) for prefix in prefixes):
                                return lines
                else:
                    line_buffer.append(byte)

            # Защита от длинной «залипшей» строки без CR/LF.
            if len(line_buffer) >= 220:
                line = line_buffer.decode("cp1251", errors="ignore").strip()
                line_buffer.clear()
                if line:
                    lines.append(line)
                    self._log("rx", line)
                    if prefixes and any(line.startswith(prefix) for prefix in prefixes):
                        return lines

        if line_buffer and len(lines) < max_lines:
            tail_line = line_buffer.decode("cp1251", errors="ignore").strip()
            if tail_line:
                lines.append(tail_line)
                self._log("rx", tail_line)
                if prefixes and any(tail_line.startswith(prefix) for prefix in prefixes):
                    return lines

        if not lines and expect_response:
            timeout_message = (
                f"Таймаут: нет ответа на '{command}' за {timeout:.1f} c "
                f"(порт {self._port}, {self._baudrate} бод). "
                "Проверьте RS-485 в свойствах COM, полярность линии A/B и общий GND."
            )
            self._log("err", timeout_message)
            LOGGER.warning(timeout_message)
            if prefixes:
                raise TimeoutError(timeout_message)

        return lines

    def _log(self, direction: str, message: str) -> None:
        """Добавляет запись в журнал обмена с отметкой времени."""
        if direction == "err":
            LOGGER.error(message)
        elif direction == "tx":
            LOGGER.info("TX %s", message)
        elif direction == "rx":
            LOGGER.info("RX %s", message)
        else:
            LOGGER.info(message)

        self._history.append(
            {
                "ts": datetime.now().strftime("%H:%M:%S"),
                "dir": direction,
                "text": message,
            }
        )


def list_available_ports() -> list[str]:
    """Возвращает список доступных COM-портов в системе."""
    ports: set[str] = set()

    if list_ports is not None:
        try:
            for port in list_ports.comports():
                value = str(getattr(port, "device", "") or "").strip().upper()
                if value.startswith("COM"):
                    ports.add(value)
        except Exception:
            pass

    if not ports:
        ports.update(_list_ports_from_windows_registry())

    if not ports:
        ports.update(_list_ports_from_mode_command())

    return sorted(ports, key=_com_sort_key)


def _com_sort_key(port_name: str) -> tuple[int, str]:
    """Возвращает ключ сортировки COM-портов по числу, затем по строке."""
    match = re.match(r"^COM(\d+)$", str(port_name).strip().upper())
    if not match:
        return (10_000, str(port_name).upper())
    return (int(match.group(1)), str(port_name).upper())


def _list_ports_from_windows_registry() -> set[str]:
    """Пытается прочитать COM-порты из реестра Windows как fallback."""
    if winreg is None:
        return set()

    result: set[str] = set()
    key_path = r"HARDWARE\DEVICEMAP\SERIALCOMM"

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            index = 0
            while True:
                try:
                    _, value, _ = winreg.EnumValue(key, index)
                except OSError:
                    break
                port_name = str(value).strip().upper()
                if port_name.startswith("COM"):
                    result.add(port_name)
                index += 1
    except OSError:
        return set()

    return result


def _list_ports_from_mode_command() -> set[str]:
    """Пытается извлечь COM-порты из вывода команды mode в Windows."""
    result: set[str] = set()
    try:
        completed = subprocess.run(
            ["cmd", "/c", "mode"],
            capture_output=True,
            text=True,
            check=False,
            encoding="cp866",
            errors="ignore",
        )
    except Exception:
        return result

    output = (completed.stdout or "") + "\n" + (completed.stderr or "")
    for match in re.finditer(r"Status\s+for\s+device\s+(COM\d+):", output, flags=re.IGNORECASE):
        result.add(match.group(1).upper())

    return result
