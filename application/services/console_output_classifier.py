from application.services.console_line_type import ConsoleLineType
from application.services.console_output_markers import (
    SYSTEM_MARKERS,
    SUCCESS_MARKERS,
    ERROR_MARKERS,
    WARNING_MARKERS,
    )


def classify_console_line(text: str) -> ConsoleLineType:
    """
    Классифицирует строку вывода ping для отображения.

    Application-layer сервис.
    Не использует Domain.
    Не знает про UI и цвета.
    """

    if not text:
        return ConsoleLineType.INFO

    t = text.lower()

    # --- SYSTEM ---
    if any(marker in t for marker in SYSTEM_MARKERS):
        return ConsoleLineType.SYSTEM

    # --- ERROR (приоритет над SUCCESS) ---
    if any(marker in t for marker in ERROR_MARKERS):
        return ConsoleLineType.ERROR

    # --- SUCCESS ---
    if any(marker in t for marker in SUCCESS_MARKERS):
        return ConsoleLineType.SUCCESS

    # --- WARNING ---
    if any(marker in t for marker in WARNING_MARKERS):
        return ConsoleLineType.WARNING

    # --- INFO ---
    return ConsoleLineType.INFO
