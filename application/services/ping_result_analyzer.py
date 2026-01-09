from domain.value_objects.ping_status import PingStatus


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


def analyze_ping_result(stdout: str, exit_code: int | None) -> PingStatus:
    if exit_code is None:
        return PingStatus.ERROR

    if not stdout or not stdout.strip():
        return PingStatus.ERROR

    has_reply = False

    for line in stdout.splitlines():
        l = line.lower()

        if any(m in l for m in UNREACHABLE_MARKERS):
            return PingStatus.FAILURE

        if any(m in l for m in REPLY_MARKERS):
            has_reply = True

    if has_reply:
        return PingStatus.SUCCESS

    if exit_code == 0:
        return PingStatus.ERROR

    return PingStatus.FAILURE
