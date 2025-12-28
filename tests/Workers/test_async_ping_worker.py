import pytest
import asyncio
from unittest.mock import patch, AsyncMock

from Workers.async_ping_worker import AsyncPingWorker

@pytest.mark.asyncio
async def test_ping_ip_success():
    worker = AsyncPingWorker(["127.0.0.1"])

    # Мокаем subprocess
    mock_proc = AsyncMock()
    mock_proc.returncode = 0
    with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
        result = []
        worker.ping_result.connect(lambda ip, success: result.append((ip, success)))
        await worker.ping_ip("127.0.0.1")
        assert result == [("127.0.0.1", True)]

@pytest.mark.asyncio
async def test_ping_ip_fail():
    worker = AsyncPingWorker(["192.0.2.1"])

    mock_proc = AsyncMock()
    mock_proc.returncode = 1
    with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
        result = []
        worker.ping_result.connect(lambda ip, success: result.append((ip, success)))
        await worker.ping_ip("192.0.2.1")
        assert result == [("192.0.2.1", False)]

@pytest.mark.asyncio
async def test_run_async_progress_and_finished():
    ips = ["127.0.0.1", "192.0.2.1"]
    worker = AsyncPingWorker(ips, max_concurrent=1)

    mock_proc = AsyncMock()
    mock_proc.returncode = 0
    with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
        progress_updates = []
        finished_flag = []

        worker.progress.connect(lambda val: progress_updates.append(val))
        worker.finished.connect(lambda: finished_flag.append(True))

        await worker.run_async()

        # Проверяем, что прогресс достиг 100%
        assert progress_updates[-1] == 100
        # Проверяем, что finished сигнал сработал
        assert finished_flag == [True]
