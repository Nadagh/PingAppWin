import asyncio
import platform
from typing import List, Tuple


class AsyncPingExecutor:
    """
    Асинхронный executor ping через ОС.
    Возвращает exit code и stdout.
    """

    async def ping_with_output(
        self,
        ip: str,
        count: int = 1,
        timeout_ms: int = 1000,
    ) -> Tuple[int, List[str]]:

        system = platform.system().lower()
        encoding = "cp866" if system == "windows" else "utf-8"

        if system == "windows":
            cmd = ["ping", "-n", str(count), "-w", str(timeout_ms), ip]
        else:
            timeout_s = max(1, timeout_ms // 1000)
            cmd = ["ping", "-c", str(count), "-W", str(timeout_s), ip]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            output: list[str] = []
            assert proc.stdout is not None

            async for raw in proc.stdout:
                output.append(
                    raw.decode(encoding, errors="replace").strip()
                )

            exit_code = await proc.wait()
            return exit_code, output

        except Exception:
            return 2, []
