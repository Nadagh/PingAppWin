# domain/services/ping_rules.py

from domain.value_objects.ping_status import PingStatus


def status_from_exit_code(exit_code: int) -> PingStatus:
    """
    Преобразует код возврата ping в доменный статус.
    """
    if exit_code == 0:
        return PingStatus.SUCCESS
    if exit_code == 1:
        return PingStatus.FAILURE
    return PingStatus.ERROR
