# tests/domain/test_ping_result_status.py

from enum import Enum

from domain.value_objects.ping_result_status import PingResultStatus


def test_ping_result_status_is_enum():
    assert issubclass(PingResultStatus, Enum)


def test_all_expected_statuses_exist():
    """
    Domain contract.

    Любое изменение этого списка — изменение доменной модели
    и должно быть осознанным.
    """

    expected = {
        "PENDING",
        "SUCCESS",
        "UNSTABLE",
        "UNREACHABLE",
        "TIMEOUT",
        "HOST_NOT_FOUND",
        "INVALID_ADDRESS",
        "ERROR",
        "MISSING_ADDRESS",
    }

    actual = {status.name for status in PingResultStatus}

    assert actual == expected


def test_statuses_are_unique():
    values = [status.value for status in PingResultStatus]
    assert len(values) == len(set(values))


def test_enum_string_representation_is_stable():
    """
    Защита от auto()/рефакторинга:
    имя enum — часть внешнего контракта.
    """
    status = PingResultStatus.UNSTABLE
    assert status.name == "UNSTABLE"
