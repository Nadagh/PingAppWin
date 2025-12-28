import asyncio
import platform


class AsyncPingExecutor:
    """
    Асинхронный executor ping через ОС.
    Возвращает exit code.
    """

    async def ping(self, ip: str, count: int = 1) -> int:
        system = platform.system().lower()
        if system == "windows":
            cmd = ["ping", "-n", str(count), ip]
        else:
            cmd = ["ping", "-c", str(count), ip]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            return await proc.wait()
        except Exception:
            return 2
