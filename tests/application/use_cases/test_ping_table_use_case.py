# tests/application/use_cases/test_ping_table_use_case.py

from unittest.mock import Mock
import pytest

from application.use_cases.ping_table import PingTableUseCase
from domain.value_objects.ping_result_status import PingResultStatus


class TestPingTableUseCase:

    def test_empty_ip_results_in_missing_address(self, monkeypatch):
        fake_executor = Mock()

        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutorPort",
            lambda: fake_executor,
        )

        use_case = PingTableUseCase()
        result = use_case.prepare_ping([""])

        assert result == [
            ("", PingResultStatus.MISSING_ADDRESS),
        ]

        fake_executor.ping.assert_not_called()


    def test_invalid_ip_results_in_invalid_address(self, monkeypatch):
        fake_executor = Mock()

        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutorPort",
            lambda: fake_executor,
        )

        use_case = PingTableUseCase()
        result = use_case.prepare_ping(["abc"])

        assert result == [
            ("abc", PingResultStatus.INVALID_ADDRESS),
        ]

        fake_executor.ping.assert_not_called()


    def test_valid_ip_success(self, monkeypatch):
        fake_executor = Mock()
        fake_executor.ping.return_value = 0

        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutorPort",
            lambda: fake_executor,
        )

        use_case = PingTableUseCase()
        result = use_case.prepare_ping(["127.0.0.1"])

        assert result == [
            ("127.0.0.1", PingResultStatus.SUCCESS),
        ]

        fake_executor.ping.assert_called_once_with("127.0.0.1", count=1)


    def test_valid_ip_unreachable(self, monkeypatch):
        fake_executor = Mock()
        fake_executor.ping.return_value = 1

        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutorPort",
            lambda: fake_executor,
        )

        use_case = PingTableUseCase()
        result = use_case.prepare_ping(["10.255.255.1"])

        assert result == [
            ("10.255.255.1", PingResultStatus.UNREACHABLE),
        ]


    def test_multiple_ips_preserve_order(self, monkeypatch):
        fake_executor = Mock()
        fake_executor.ping.return_value = 0

        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutorPort",
            lambda: fake_executor,
        )

        use_case = PingTableUseCase()
        result = use_case.prepare_ping([
            "",
            "127.0.0.1",
            "abc",
        ])

        assert result == [
            ("", PingResultStatus.MISSING_ADDRESS),
            ("127.0.0.1", PingResultStatus.SUCCESS),
            ("abc", PingResultStatus.INVALID_ADDRESS),
        ]


    def test_executor_exception_results_in_error(self, monkeypatch):
        def boom(*args, **kwargs):
            raise RuntimeError("ping failed")

        fake_executor = Mock()
        fake_executor.ping.side_effect = boom

        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutorPort",
            lambda: fake_executor,
        )

        use_case = PingTableUseCase()
        result = use_case.prepare_ping(["8.8.8.8"])

        assert result == [
            ("8.8.8.8", PingResultStatus.ERROR),
        ]
