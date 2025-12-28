# infrastructure/ping/ping_executor.py

import subprocess
import platform


class PingExecutor:
    """
    Infrastructure service.
    Выполняет реальный ping через ОС.
    """

    def ping(self, ip: str, count: int = 1) -> int:
        """
        Возвращает exit code ping-команды.
        """
        system = platform.system().lower()

        if system == "windows":
            cmd = ["ping", "-n", str(count), ip]
        else:
            cmd = ["ping", "-c", str(count), ip]

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return result.returncode
        except Exception:
            return 2  # аварийный код, интерпретируется Domain
