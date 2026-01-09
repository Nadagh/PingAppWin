from domain.value_objects.ping_result_status import PingResultStatus
from application.services.ping_result_markers import *





def analyze_ping_result(stdout: str, exit_code: int | None) -> PingResultStatus:
    if exit_code is None:
        return PingResultStatus.ERROR

    if not stdout or not stdout.strip():
        return PingResultStatus.ERROR

    echo_replies = 0
    unreachable_count = 0
    timeout_count = 0
    general_failure_count = 0

    for line in stdout.splitlines():
        l = line.lower()

        if any(m in l for m in INVALID_ADDRESS_MARKERS):
            return PingResultStatus.INVALID_ADDRESS

        if any(m in l for m in HOST_NOT_FOUND_MARKERS):
            return PingResultStatus.HOST_NOT_FOUND

        if any(m in l for m in GENERAL_FAILURE_MARKERS):
            general_failure_count += 1
            continue

        if any(m in l for m in UNREACHABLE_MARKERS):
            unreachable_count += 1
            continue

        if any(m in l for m in TIMEOUT_MARKERS):
            timeout_count += 1
            continue

        if any(m in l for m in REPLY_MARKERS):
            echo_replies += 1

    # ===== UNSTABLE =====

    # General failure + что угодно живое → нестабильно
    if general_failure_count > 0 and echo_replies > 0:
        return PingResultStatus.UNSTABLE

    # Повторяющиеся сбои + ответы → нестабильно
    if echo_replies > 0 and (
        unreachable_count > 1
        or timeout_count > 1
    ):
        return PingResultStatus.UNSTABLE

    # ===== ПРИОРИТЕТНЫЕ СОСТОЯНИЯ =====

    if unreachable_count > 0:
        return PingResultStatus.UNREACHABLE

    if timeout_count > 0:
        return PingResultStatus.TIMEOUT

    if echo_replies > 0:
        return PingResultStatus.SUCCESS

    if general_failure_count > 0:
        return PingResultStatus.ERROR

    return PingResultStatus.ERROR
