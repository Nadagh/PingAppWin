from application.services.console_line_type import ConsoleLineType


def classify_console_line(text: str) -> ConsoleLineType:
    """
    Классифицирует строку вывода ping для отображения.

    НЕ использует Domain.
    НЕ знает про цвета.
    НЕ знает про UI.

    Возвращает ConsoleLineType.
    """

    if not text:
        return ConsoleLineType.INFO

    t = text.lower()

    # --- SYSTEM ---
    if (
            "запуск ping" in t
            or "режим:" in t
            or "control + break" in t
            or "обмен пакетами" in t
            or "статистика ping" in t
    ):
        return ConsoleLineType.SYSTEM

    # --- SUCCESS ---
    if (
            "ttl=" in t
            or "bytes=" in t
            or "число байт" in t
    ):
        return ConsoleLineType.SUCCESS

    # --- ERROR ---
    if (
            "timeout" in t
            or "превышен" in t
            or "unreachable" in t
            or "сбой" in t
            or "не удается" in t
            or "could not find host" in t
            or "ошибка" in t
            or "unreachable" in t
            or "недоступен" in t
            or "destination host unreachable" in t
            or "неверный ip" in t
            or "invalid ip" in t

    ):
        return ConsoleLineType.ERROR

    # --- WARNING ---
    if "loss" in t or "потер" in t:
        return ConsoleLineType.WARNING

    # --- INFO ---
    return ConsoleLineType.INFO
