import subprocess
import platform

from infrastructure.ping.ping_executor import PingExecutor


def test_ping_executor_returns_exit_code(monkeypatch):
    class FakeResult:
        returncode = 0

    def fake_run(*args, **kwargs):
        return FakeResult()

    monkeypatch.setattr(subprocess, "run", fake_run)

    executor = PingExecutor()
    code = executor.ping("8.8.8.8", count=1)

    assert code == 0


def test_ping_executor_handles_exception(monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("ping failed")

    monkeypatch.setattr(subprocess, "run", boom)

    executor = PingExecutor()
    code = executor.ping("8.8.8.8", count=1)

    # аварийный код
    assert code == 2
