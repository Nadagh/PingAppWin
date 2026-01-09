import pytest
from application import NetworkScanUseCase
from unittest.mock import AsyncMock
fake_executor = AsyncMock()


@pytest.mark.asyncio
async def test_scan_calls_executor_for_each_ip(mocker):
    fake_executor = mocker.AsyncMock()
    fake_executor.ping.return_value = True

    use_case = NetworkScanUseCase(ping_executor=fake_executor)

    await use_case.execute(
        raw_ranges="10.0.0.1-2",
        count=1,
        max_parallel=10,
        on_progress=lambda *_: None,
        on_result=lambda *_: None,
    )

    assert fake_executor.ping.await_count == 2

@pytest.mark.asyncio
async def test_results_are_reported(mocker):
    fake_executor = mocker.AsyncMock()
    fake_executor.ping.side_effect = [True, False]

    results = []

    use_case = NetworkScanUseCase(ping_executor=fake_executor)

    await use_case.execute(
        raw_ranges="10.0.0.1-2",
        count=1,
        max_parallel=10,
        on_progress=lambda *_: None,
        on_result=lambda ip, alive: results.append((ip, alive)),
    )

    assert results == [
        ("10.0.0.1", True),
        ("10.0.0.2", False),
    ]

@pytest.mark.asyncio
async def test_progress_is_reported(mocker):
    fake_executor = mocker.AsyncMock()
    fake_executor.ping.return_value = True

    progress = []

    use_case = NetworkScanUseCase(ping_executor=fake_executor)

    await use_case.execute(
        raw_ranges="10.0.0.1-3",
        count=1,
        max_parallel=10,
        on_progress=lambda done, total: progress.append((done, total)),
        on_result=lambda *_: None,
    )

    assert progress[-1] == (3, 3)

@pytest.mark.asyncio
async def test_empty_ranges_report_zero_progress(mocker):
    progress = []

    use_case = NetworkScanUseCase(ping_executor=mocker.AsyncMock())

    await use_case.execute(
        raw_ranges="",
        count=1,
        max_parallel=10,
        on_progress=lambda d, t: progress.append((d, t)),
        on_result=lambda *_: None,
    )

    assert progress == [(0, 0)]

@pytest.mark.asyncio
async def test_invalid_ranges_raise_value_error(mocker):
    use_case = NetworkScanUseCase(ping_executor=mocker.AsyncMock())

    with pytest.raises(ValueError):
        await use_case.execute(
            raw_ranges="abc",
            count=1,
            max_parallel=10,
            on_progress=lambda *_: None,
            on_result=lambda *_: None,
        )

@pytest.mark.asyncio
async def test_ping_exception_reported_as_dead_host(mocker):
    fake_executor = mocker.AsyncMock()
    fake_executor.ping.side_effect = RuntimeError("boom")

    results = []

    use_case = NetworkScanUseCase(ping_executor=fake_executor)

    await use_case.execute(
        raw_ranges="10.0.0.1",
        count=1,
        max_parallel=1,
        on_progress=lambda *_: None,
        on_result=lambda ip, alive: results.append((ip, alive)),
    )

    assert results == [("10.0.0.1", False)]


