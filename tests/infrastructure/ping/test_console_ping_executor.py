import subprocess
import platform

from infrastructure.ping.console_ping_executor import ConsolePingExecutor


def test_console_ping_executor_streams_output(monkeypatch):
    lines = [
        "Reply from 8.8.8.8\n",
        "TTL=64\n",
    ]

    class FakeProcess:
        def __init__(self):
            self.stdout = iter(lines)

        def wait(self):
            return 0

        def poll(self):
            return 0

    def fake_popen(*args, **kwargs):
        return FakeProcess()

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    output = []

    def on_output(line: str):
        output.append(line)

    executor = ConsolePingExecutor()
    executor.run(
        ip="8.8.8.8",
        count=1,
        timeout_ms=1000,
        on_output=on_output,
    )

    assert output == ["Reply from 8.8.8.8", "TTL=64"]


def test_console_ping_executor_handles_start_failure(monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("spawn failed")

    monkeypatch.setattr(subprocess, "Popen", boom)

    output = []

    def on_output(line: str):
        output.append(line)

    executor = ConsolePingExecutor()
    executor.run(
        ip="8.8.8.8",
        count=1,
        timeout_ms=1000,
        on_output=on_output,
    )

    assert any("Ошибка запуска ping" in line for line in output)
