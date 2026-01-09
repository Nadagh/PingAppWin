import pytest
from unittest.mock import Mock

from application.use_cases.ping_table import PingTableUseCase
from domain import PingStatus


class TestPingTableUseCase:
    def test_empty_ip_results_in_missing(self, monkeypatch):
        use_case = PingTableUseCase()

        fake_executor = Mock()
        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutor",
            lambda: fake_executor,
        )

        result = use_case.prepare_ping([""])

        assert result == [
            ("", PingStatus.MISSING),
        ]
        fake_executor.ping.assert_not_called()

    def test_invalid_ip_results_in_error(self, monkeypatch):
        use_case = PingTableUseCase()

        fake_executor = Mock()
        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutor",
            lambda: fake_executor,
        )

        result = use_case.prepare_ping(["abc"])

        assert result == [
            ("abc", PingStatus.ERROR),
        ]
        fake_executor.ping.assert_not_called()

    def test_valid_ip_success(self, monkeypatch):
        fake_executor = Mock()
        fake_executor.ping.return_value = 0

        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutor",
            lambda: fake_executor,
        )

        use_case = PingTableUseCase()
        result = use_case.prepare_ping(["127.0.0.1"])

        assert result == [
            ("127.0.0.1", PingStatus.SUCCESS),
        ]

        fake_executor.ping.assert_called_once_with("127.0.0.1", count=1)

    def test_valid_ip_failure(self, monkeypatch):
        fake_executor = Mock()
        fake_executor.ping.return_value = 1

        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutor",
            lambda: fake_executor,
        )

        use_case = PingTableUseCase()
        result = use_case.prepare_ping(["10.255.255.1"])

        assert result == [
            ("10.255.255.1", PingStatus.FAILURE),
        ]

        fake_executor.ping.assert_called_once_with("10.255.255.1", count=1)

    def test_multiple_ips_preserve_order(self, monkeypatch):
        fake_executor = Mock()
        fake_executor.ping.return_value = 0

        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutor",
            lambda: fake_executor,
        )

        use_case = PingTableUseCase()
        result = use_case.prepare_ping([
            "",
            "127.0.0.1",
            "abc",
        ])

        assert result == [
            ("", PingStatus.MISSING),
            ("127.0.0.1", PingStatus.SUCCESS),
            ("abc", PingStatus.ERROR),
        ]

        fake_executor.ping.assert_called_once_with("127.0.0.1", count=1)

    def test_executor_exception_results_in_error(self, monkeypatch):
        def boom(*args, **kwargs):
            raise RuntimeError("ping failed")

        fake_executor = Mock()
        fake_executor.ping.side_effect = boom

        monkeypatch.setattr(
            "application.use_cases.ping_table.PingExecutor",
            lambda: fake_executor,
        )

        use_case = PingTableUseCase()
        result = use_case.prepare_ping(["8.8.8.8"])

        assert result == [
            ("8.8.8.8", PingStatus.ERROR),
        ]

        fake_executor.ping.assert_called_once_with("8.8.8.8", count=1)
