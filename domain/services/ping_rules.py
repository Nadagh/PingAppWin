from domain.value_objects.ping_status import PingStatus


def status_from_exit_code(exit_code: int) -> PingStatus:
    if exit_code is None:
        return PingStatus.ERROR

    if not isinstance(exit_code, int):
        raise TypeError(f"exit_code must be int, got {type(exit_code)}")

    if exit_code == 0:
        return PingStatus.SUCCESS

    if exit_code in (1, 2):
        return PingStatus.FAILURE

    return PingStatus.ERROR
