import pytest
import platform

from infrastructure.ping.async_ping_executor import AsyncPingExecutor


@pytest.mark.asyncio
async def test_windows_cp866_ping_output_decoded_correctly(monkeypatch):
    """
    Windows (RU):
    stdout ping приходит в cp866.
    Проверяем, что AsyncPingExecutor НЕ ломает кириллицу.
    """

    if platform.system().lower() != "windows":
        pytest.skip("Тест актуален только для Windows")

    # --- реальный вывод ping 127.0.0.1 (фрагмент) ---
    text = (
        "Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128\n"
        "Статистика Ping для 127.0.0.1:\n"
        "    Пакетов: отправлено = 1, получено = 1, потеряно = 0\n"
    )

    # кодируем как это делает Windows
    raw_bytes = text.encode("cp866")

    # --- fake process stdout ---
    class FakeStdout:
        def __aiter__(self):
            async def gen():
                for line in raw_bytes.splitlines(keepends=True):
                    yield line
            return gen()

    class FakeProcess:
        stdout = FakeStdout()

        async def wait(self):
            return 0

    async def fake_create_subprocess_exec(*args, **kwargs):
        return FakeProcess()

    monkeypatch.setattr(
        "asyncio.create_subprocess_exec",
        fake_create_subprocess_exec,
    )

    executor = AsyncPingExecutor()
    exit_code, output = await executor.ping_with_output("127.0.0.1")

    assert exit_code == 0

    joined = "\n".join(output)

    # 🔥 ключевые маркеры, которые раньше ломались
    assert "Ответ от 127.0.0.1" in joined
    assert "число байт" in joined
    assert "TTL=128" in joined
