import pytest
import asyncio

from infrastructure.ping.async_ping_executor import AsyncPingExecutor


@pytest.mark.asyncio
async def test_async_ping_executor_returns_exit_code_and_output(monkeypatch):
    class FakeStdout:
        def __aiter__(self):
            async def gen():
                yield b"reply\n"
            return gen()

    class FakeProc:
        stdout = FakeStdout()

        async def wait(self):
            return 0

    async def fake_exec(*args, **kwargs):
        return FakeProc()

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_exec)

    executor = AsyncPingExecutor()
    code, output = await executor.ping_with_output("8.8.8.8")

    assert code == 0
    assert output == ["reply"]


@pytest.mark.asyncio
async def test_async_ping_executor_handles_exception(monkeypatch):
    async def boom(*args, **kwargs):
        raise RuntimeError("exec failed")

    monkeypatch.setattr(asyncio, "create_subprocess_exec", boom)

    executor = AsyncPingExecutor()
    code, output = await executor.ping_with_output("8.8.8.8")

    assert code == 2
    assert output == []
