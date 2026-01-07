from domain import PingStatus


UNREACHABLE_MARKERS = (
    "unreachable",
    "недоступен",
    "destination host unreachable",
    "заданный узел",
)

REPLY_MARKERS = (
    "ttl=",
    "time=",
    "icmp_seq",
    "bytes=",
    "число байт",
)


def analyze_ping_result(exit_code: int, output: list[str]) -> PingStatus:
    """
    SUCCESS:
    - есть ICMP Echo Reply от целевого узла
    - и НЕТ ICMP Unreachable

    FAILURE:
    - есть хотя бы один ICMP Unreachable
    - или нет reply
    """

    has_reply = False

    for line in output:
        l = line.lower()

        # Любой unreachable = немедленный отказ
        if any(m in l for m in UNREACHABLE_MARKERS):
            return PingStatus.FAILURE

        # Только реальный Echo Reply
        if any(m in l for m in REPLY_MARKERS):
            has_reply = True

    if has_reply:
        return PingStatus.SUCCESS

    return PingStatus.FAILURE
