from application.services.console_line_type import ConsoleLineType


SYSTEM_MARKERS = (
    "запуск ping",
    "режим:",
    "control + break",
    "обмен пакетами",
    "статистика ping",
    "ping statistics",
)

SUCCESS_MARKERS = (
    "ttl=",
    "bytes=",
    "число байт",
)

ERROR_MARKERS = (
    "request timed out",
    "timeout",
    "превышен",
    "unreachable",
    "сбой",
    "не удается",
    "could not find host",
    "ошибка",
    "недоступен",
    "неверный ip",
    "invalid ip",
)

WARNING_MARKERS = (
    "loss",
    "потер",
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
