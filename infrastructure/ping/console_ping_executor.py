# infrastructure/ping/console_ping_executor.py

import subprocess
import platform
from typing import Callable, Optional


class ConsolePingExecutor:
    """
    Infrastructure-level executor для консольного ping.

    Ответственность:
    - запуск системной утилиты ping
    - построчное чтение stdout
    - передача строк через callback

    НЕ знает:
    - Domain
    - Qt
    - Presenter
    """

    def run(
        self,
        ip: str,
        count: Optional[int],
        on_output: Callable[[str], None],
    ) -> None:
        """
        Запускает ping и передаёт вывод построчно.

        :param ip: IP адрес (строка, предполагается валидной)
        :param count: количество пакетов или None для бесконечного режима
        :param on_output: callback для каждой строки stdout
        """
        system = platform.system().lower()

        if system == "windows":
            if count is None:
                cmd = ["ping", ip]
            else:
                cmd = ["ping", "-n", str(count), ip]
        else:
            if count is None:
                cmd = ["ping", ip]
            else:
                cmd = ["ping", "-c", str(count), ip]

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            assert process.stdout is not None

            for line in process.stdout:
                on_output(line.rstrip())

            process.wait()

        except Exception as exc:
            on_output(f"Ошибка запуска ping: {exc}")
