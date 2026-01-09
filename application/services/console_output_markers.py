# application/services/console_output_markers.py

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

    # Windows RU ConsoleTab
    "не удалось обнаружить узел",
    "проверьте имя узла",
)

WARNING_MARKERS = (
    "loss",
    "потер",
)
