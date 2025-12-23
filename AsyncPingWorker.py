import asyncio
import platform
import subprocess
import re


class AsyncPingWorker:
    """
    Асинхронный воркер пинга. Возвращает True если хотя бы один пакет прошёл.
    """

    def __init__(self, ip: str, count: int):
        self.ip = ip
        self.count = count

    async def run(self) -> bool:
        """
        Асинхронный метод запуска пинга.
        """
        # Определяем команду в зависимости от платформы
        system = platform.system()
        if system == "Windows":
            cmd = ["ping", self.ip, "-n", str(self.count)]
        else:
            cmd = ["ping", self.ip, "-c", str(self.count)]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )

            success = False
            while True:
                line = await proc.stdout.readline()
                if not line:
                    break

                try:
                    text = line.decode("cp866").strip()
                except Exception:
                    text = line.decode(errors="ignore").strip()

                # Проверяем успешный ping
                # Поддержка английских и русских систем
                text_l = text.lower()
                if any(k in text_l for k in ("ttl=", "time=")):
                    success = True
                elif any(k in text_l for k in ("сбой", "превышен", "timeout")):
                    pass  # Неудача, не меняем флаг

            await proc.wait()
            return success

        except Exception:
            return False
