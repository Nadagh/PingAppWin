# tests/application/use_cases/test_async_ping_table_use_case.py

from unittest.mock import AsyncMock
import pytest

from application.use_cases.async_ping_table import AsyncPingTableUseCase
from domain.value_objects.ping_result_status import PingResultStatus


@pytest.mark.asyncio
class TestAsyncPingTableUseCase:

    async def test_empty_ip_results_in_missing_address(self):
        results = []

        def on_result(row, status):
            results.append((row, status))

        use_case = AsyncPingTableUseCase(on_result=on_result)
        await use_case.run([""])

        assert (0, PingResultStatus.MISSING_ADDRESS) in results
        assert len(results) == 1


    async def test_invalid_ip_results_in_invalid_address(self):
        results = []

        def on_result(row, status):
            results.append((row, status))

        use_case = AsyncPingTableUseCase(on_result=on_result)
        await use_case.run(["abc"])

        assert (0, PingResultStatus.INVALID_ADDRESS) in results
        assert len(results) == 1


    async def test_valid_ip_emits_pending_and_success(self, monkeypatch):
        results = []

        def on_result(row, status):
            results.append((row, status))

        fake_executor = AsyncMock()
        fake_executor.ping_with_output.return_value = (
            0,
            ["Reply from 127.0.0.1: bytes=32 time=1ms TTL=128"],
        )

        monkeypatch.setattr(
            "application.use_cases.async_ping_table.AsyncPingExecutor",
            lambda: fake_executor,
        )

        monkeypatch.setattr(
            "application.use_cases.async_ping_table.analyze_ping_result",
            lambda stdout, exit_code: PingResultStatus.SUCCESS,
        )

        use_case = AsyncPingTableUseCase(on_result=on_result)
        await use_case.run(["127.0.0.1"])

        statuses = [status for _, status in results]

        assert PingResultStatus.PENDING in statuses
        assert PingResultStatus.SUCCESS in statuses
        assert len(results) == 2

        fake_executor.ping_with_output.assert_awaited_once()


    async def test_cancel_prevents_execution(self, monkeypatch):
        results = []

        def on_result(row, status):
            results.append((row, status))

        fake_executor = AsyncMock()

        monkeypatch.setattr(
            "application.use_cases.async_ping_table.AsyncPingExecutor",
            lambda: fake_executor,
        )

        use_case = AsyncPingTableUseCase(on_result=on_result)
        use_case.cancel()

        await use_case.run(["127.0.0.1"])

        assert results == []
        fake_executor.ping_with_output.assert_not_called()


    async def test_multiple_ips_are_independent(self, monkeypatch):
        results = []

        def on_result(row, status):
            results.append((row, status))

        fake_executor = AsyncMock()
        fake_executor.ping_with_output.side_effect = [
            (0, ["reply"]),
            (1, ["Request timed out"]),
        ]

        monkeypatch.setattr(
            "application.use_cases.async_ping_table.AsyncPingExecutor",
            lambda: fake_executor,
        )

        monkeypatch.setattr(
            "application.use_cases.async_ping_table.analyze_ping_result",
            lambda stdout, exit_code:
                PingResultStatus.SUCCESS
                if exit_code == 0
                else PingResultStatus.TIMEOUT,
        )

        use_case = AsyncPingTableUseCase(on_result=on_result)
        await use_case.run(["127.0.0.1", "10.255.255.1"])

        # группируем по строкам
        by_row = {}
        for row, status in results:
            by_row.setdefault(row, set()).add(status)

        assert by_row[0] == {
            PingResultStatus.PENDING,
            PingResultStatus.SUCCESS,
        }

        assert by_row[1] == {
            PingResultStatus.PENDING,
            PingResultStatus.TIMEOUT,
        }
