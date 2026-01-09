# tests/domain/test_ping_rules.py

import pytest

from domain.value_objects.ping_status import PingStatus
from domain.services.ping_rules import status_from_exit_code


class TestPingRules:
    """Domain tests for ping exit code interpretation."""

    @pytest.mark.parametrize(
        "exit_code",
        [0],
    )
    def test_exit_code_zero_means_success(self, exit_code: int):
        status = status_from_exit_code(exit_code)
        assert status == PingStatus.SUCCESS

    @pytest.mark.parametrize(
        "exit_code",
        [
            1,   # generic failure (host unreachable, timeout on Windows)
            2,   # malformed arguments or other ping error
        ],
    )
    def test_known_non_zero_exit_codes_mean_failure(self, exit_code: int):
        status = status_from_exit_code(exit_code)
        assert status == PingStatus.FAILURE

    @pytest.mark.parametrize(
        "exit_code",
        [
            -1,
            255,
            999,
        ],
    )
    def test_unknown_exit_codes_are_mapped_to_error(self, exit_code: int):
        status = status_from_exit_code(exit_code)
        assert status == PingStatus.ERROR

    def test_exit_code_must_be_int(self):
        with pytest.raises(TypeError):
            status_from_exit_code("0")  # type: ignore

    def test_none_exit_code_is_error(self):
        status = status_from_exit_code(None)  # type: ignore
        assert status == PingStatus.ERROR
