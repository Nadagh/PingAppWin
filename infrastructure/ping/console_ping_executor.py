import platform
import signal
import subprocess
import time
from typing import Callable, Optional


class ConsolePingExecutor:
    def __init__(self) -> None:
        self._process: subprocess.Popen | None = None
        self._stopped: bool = False


    def run(
            self,
            ip: str,
            count: Optional[int],
            timeout_ms: int,
            on_output: Callable[[str], None],
            ) -> None:

        system = platform.system().lower()
        encoding = "cp866" if system == "windows" else "utf-8"

        if system == "windows":
            if count is None:
                cmd = ["ping", "-t", "-w", str(timeout_ms), ip]
            else:
                cmd = ["ping", "-n", str(count), "-w", str(timeout_ms), ip]

        else:
            timeout_s = max(1, timeout_ms // 1000)
            if count is None:
                cmd = ["ping", "-W", str(timeout_s), ip]
            else:
                cmd = ["ping", "-c", str(count), "-W", str(timeout_s), ip]

        self._stopped = False

        try:
            self._process = subprocess.Popen(
                    cmd,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.STDOUT,
                    text = True,
                    encoding = encoding,
                    errors = "replace",
                    creationflags = (
                            subprocess.CREATE_NEW_PROCESS_GROUP
                            if system == "windows"
                            else 0
                    ),
                    )

            assert self._process.stdout is not None

            # Читаем stdout до EOF
            for line in self._process.stdout:
                on_output(line.rstrip())

            self._process.wait()

        except Exception as exc:
            on_output(f"Ошибка запуска ping: {exc}")

        finally:
            self._process = None
            self._stopped = False


    def stop(self) -> None:
        if not self._process or self._stopped:
            return

        self._stopped = True
        system = platform.system().lower()

        try:
            if system == "windows":
                # 1. Мягкая остановка для статистики
                self._process.send_signal(signal.CTRL_BREAK_EVENT)

                # 2. Даём ping шанс завершиться
                time.sleep(0.3)

                # 3. Если всё ещё жив — убиваем
                if self._process.poll() is None:
                    self._process.terminate()
            else:
                self._process.send_signal(signal.SIGINT)
        except Exception:
            pass
