import pytest
import asyncio
import platform

from infrastructure.ping.async_ping_executor import AsyncPingExecutor


@pytest.mark.asyncio
async def test_windows_ru_ping_output_cp866(monkeypatch):
    if platform.system().lower() != "windows":
        pytest.skip("Windows only")

    text = (
        "Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128\n"
        "Статистика Ping для 127.0.0.1:\n"
    )
    raw = text.encode("cp866")

    class FakeStdout:
        def __aiter__(self):
            async def gen():
                for line in raw.splitlines(keepends=True):
                    yield line
            return gen()

    class FakeProc:
        stdout = FakeStdout()

        async def wait(self):
            return 0

    async def fake_exec(*args, **kwargs):
        return FakeProc()

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_exec)

    executor = AsyncPingExecutor()
    code, output = await executor.ping_with_output("127.0.0.1")

    joined = "\n".join(output)

    assert code == 0
    assert "Ответ от 127.0.0.1" in joined
    assert "число байт" in joined
    assert "TTL=128" in joined
