# tests/application/test_ping_result_analyzer.py

import pytest

from domain.value_objects.ping_status import PingStatus
from application.services.ping_result_analyzer import analyze_ping_result


class TestPingResultAnalyzer:
    """Application-level tests for ping stdout analysis."""

    def test_successful_ping(self):
        stdout = """
        Reply from 8.8.8.8: bytes=32 time=20ms TTL=117
        Reply from 8.8.8.8: bytes=32 time=21ms TTL=117

        Ping statistics for 8.8.8.8:
            Packets: Sent = 2, Received = 2, Lost = 0 (0% loss),
        """
        status = analyze_ping_result(stdout, exit_code=0)
        assert status == PingStatus.SUCCESS

    def test_destination_unreachable_is_failure(self):
        stdout = """
        Reply from 192.168.0.1: Destination host unreachable.
        Reply from 192.168.0.1: Destination host unreachable.

        Ping statistics for 192.168.0.1:
            Packets: Sent = 2, Received = 2, Lost = 0 (0% loss),
        """
        status = analyze_ping_result(stdout, exit_code=1)
        assert status == PingStatus.FAILURE

    def test_request_timed_out_is_failure(self):
        stdout = """
        Request timed out.
        Request timed out.

        Ping statistics for 10.0.0.1:
            Packets: Sent = 2, Received = 0, Lost = 2 (100% loss),
        """
        status = analyze_ping_result(stdout, exit_code=1)
        assert status == PingStatus.FAILURE

    def test_false_received_packets_are_ignored(self):
        stdout = """
        Reply from 192.168.0.1: Destination host unreachable.

        Ping statistics for 192.168.0.1:
            Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),
        """
        status = analyze_ping_result(stdout, exit_code=1)
        assert status == PingStatus.FAILURE

    def test_empty_stdout_with_nonzero_exit_code_is_error(self):
        status = analyze_ping_result("", exit_code=1)
        assert status == PingStatus.ERROR

    def test_none_exit_code_propagates_error(self):
        stdout = "Reply from 8.8.8.8: bytes=32 time=20ms TTL=117"
        status = analyze_ping_result(stdout, exit_code=None)
        assert status == PingStatus.ERROR

    def test_garbage_stdout_is_error(self):
        stdout = "some totally unrelated output"
        status = analyze_ping_result(stdout, exit_code=0)
        assert status == PingStatus.ERROR
