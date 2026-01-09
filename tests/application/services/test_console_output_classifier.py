# tests/application/services/test_console_output_classifier.py

import pytest

from application.services.console_output_classifier import classify_console_line
from application.services.console_line_type import ConsoleLineType


@pytest.mark.parametrize(
    "text, expected",
    [
        # --- SYSTEM ---
        ("Обмен пакетами с 8.8.8.8", ConsoleLineType.SYSTEM),
        ("Ping statistics for 8.8.8.8", ConsoleLineType.SYSTEM),
        ("Control + Break", ConsoleLineType.SYSTEM),
        ("Режим: бесконечный", ConsoleLineType.SYSTEM),

        # --- SUCCESS ---
        ("Reply from 8.8.8.8: bytes=32 time=20ms TTL=117", ConsoleLineType.SUCCESS),
        ("bytes=32 time=1ms ttl=64", ConsoleLineType.SUCCESS),
        ("число байт = 32", ConsoleLineType.SUCCESS),

        # --- ERROR ---
        ("Request timed out.", ConsoleLineType.ERROR),
        ("Destination host unreachable.", ConsoleLineType.ERROR),
        ("Заданный узел недоступен.", ConsoleLineType.ERROR),
        ("Не удается найти указанный узел.", ConsoleLineType.ERROR),
        ("Ошибка", ConsoleLineType.ERROR),
        ("Invalid IP address", ConsoleLineType.ERROR),

        # --- WARNING ---
        ("Lost = 1 (50% loss)", ConsoleLineType.WARNING),
        ("Потеряно = 2", ConsoleLineType.WARNING),

        # --- INFO ---
        ("Pinging google.com", ConsoleLineType.INFO),
        ("some random text", ConsoleLineType.INFO),
        ("---", ConsoleLineType.INFO),
    ],
)
def test_classify_console_line(text: str, expected: ConsoleLineType):
    assert classify_console_line(text) == expected


def test_empty_string_is_info():
    assert classify_console_line("") == ConsoleLineType.INFO


def test_none_like_text_does_not_crash():
    # защита от случайных вызовов
    assert classify_console_line(str(None)) == ConsoleLineType.INFO


def test_error_has_priority_over_success():
    text = "Reply from 8.8.8.8: Destination host unreachable."
    assert classify_console_line(text) == ConsoleLineType.ERROR
