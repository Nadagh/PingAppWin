# infrastructure/ping/console_ping_executor.py

import subprocess
import platform
from typing import Callable, Optional


class ConsolePingExecutor:
    def __init__(self) -> None:
        self._process: subprocess.Popen | None = None

    def run(
        self,
        ip: str,
        count: Optional[int],
        on_output: Callable[[str], None],
    ) -> None:
        system = platform.system().lower()
        encoding = "cp866" if system == "windows" else "utf-8"

        if system == "windows":
            cmd = ["ping", ip] if count is None else ["ping", "-n", str(count), ip]
        else:
            cmd = ["ping", ip] if count is None else ["ping", "-c", str(count), ip]

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding=encoding,
                errors="replace",
                bufsize=1,
            )

            assert self._process.stdout is not None

            for line in self._process.stdout:
                on_output(line.rstrip())

            self._process.wait()

        except Exception as exc:
            on_output(f"Ошибка запуска ping: {exc}")

    def stop(self) -> None:
        if self._process and self._process.poll() is None:
            self._process.terminate()
