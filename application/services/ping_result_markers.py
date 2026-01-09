# application/services/ping_result_markers.py

GENERAL_FAILURE_MARKERS = (
    "общий сбой",
    "general failure",
    "сбой передачи",
)

UNREACHABLE_MARKERS = (
    "destination host unreachable",
    "unreachable",
    "узел недоступен",
    "заданный узел",
)

TIMEOUT_MARKERS = (
    "request timed out",
    "превышен интервал ожидания",
    "timeout waiting",
)

HOST_NOT_FOUND_MARKERS = (
    "could not find host",
    "не удается найти указанный узел",
    "не удалось обнаружить узел",
)

INVALID_ADDRESS_MARKERS = (
    "invalid ip",
    "неверный ip",
)

REPLY_MARKERS = (
    "reply from",
    "ttl=",
    "bytes=",
    "число байт",
    "icmp_seq",
)
