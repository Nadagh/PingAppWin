# tests/application/use_cases/test_async_ping_table_use_case.py

from unittest.mock import AsyncMock, Mock

import pytest

from application.use_cases.async_ping_table import AsyncPingTableUseCase
from domain.value_objects.ping_status import PingStatus


@pytest.mark.asyncio
class TestAsyncPingTableUseCase:
    async def test_empty_ip_results_in_missing(self):
        results = []


        def on_result(row, status):
            results.append((row, status))


        use_case = AsyncPingTableUseCase(on_result = on_result)
        await use_case.run([""])

        assert results == [(0, PingStatus.MISSING)]


    async def test_invalid_ip_results_in_error(self):
        results = []


        def on_result(row, status):
            results.append((row, status))


        use_case = AsyncPingTableUseCase(on_result = on_result)
        await use_case.run(["abc"])

        assert results == [(0, PingStatus.ERROR)]


    async def test_valid_ip_goes_through_pending_and_success(self, monkeypatch):
        results = []


        def on_result(row, status):
            results.append((row, status))


        fake_executor = AsyncMock()
        fake_executor.ping_with_output.return_value = (
                0,
                ["Reply from 127.0.0.1: bytes=32 time=1ms TTL=128"],
                )

        fake_analyzer = Mock(return_value = PingStatus.SUCCESS)

        monkeypatch.setattr(
                "application.use_cases.async_ping_table.AsyncPingExecutor",
                lambda: fake_executor,
                )
        monkeypatch.setattr(
                "application.use_cases.async_ping_table.analyze_ping_result",
                fake_analyzer,
                )

        use_case = AsyncPingTableUseCase(on_result = on_result)
        await use_case.run(["127.0.0.1"])

        assert results == [
                (0, PingStatus.PENDING),
                (0, PingStatus.SUCCESS),
                ]

        fake_analyzer.assert_called_once()
        fake_executor.ping_with_output.assert_awaited_once()


    async def test_cancel_prevents_execution(self):
        results = []


        def on_result(row, status):
            results.append((row, status))


        fake_executor = AsyncMock()

        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
                "application.use_cases.async_ping_table.AsyncPingExecutor",
                lambda: fake_executor,
                )

        use_case = AsyncPingTableUseCase(on_result = on_result)
        use_case.cancel()

        await use_case.run(["127.0.0.1"])

        assert results == []
        fake_executor.ping_with_output.assert_not_called()

        monkeypatch.undo()


    async def test_multiple_ips_are_independent(self):
        results = []


        def on_result(row, status):
            results.append((row, status))


        fake_executor = AsyncMock()
        fake_executor.ping_with_output.side_effect = [
                (0, ["reply"]),
                (1, ["Request timed out"]),
                ]

        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
                "application.use_cases.async_ping_table.AsyncPingExecutor",
                lambda: fake_executor,
                )

        monkeypatch.setattr(
                "application.use_cases.async_ping_table.analyze_ping_result",
                lambda stdout, exit_code:
                PingStatus.SUCCESS if exit_code == 0 else PingStatus.FAILURE,
                )

        use_case = AsyncPingTableUseCase(on_result = on_result)
        await use_case.run(["127.0.0.1", "10.255.255.1"])

        assert (0, PingStatus.PENDING) in results
        assert (1, PingStatus.PENDING) in results
        assert (0, PingStatus.SUCCESS) in results
        assert (1, PingStatus.FAILURE) in results
        assert results.count((0, PingStatus.PENDING)) == 1
        assert results.count((1, PingStatus.PENDING)) == 1

        monkeypatch.undo()
