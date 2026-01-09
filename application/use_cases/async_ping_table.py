import asyncio

from domain import IPAddress, PingStatus
from infrastructure import AsyncPingExecutor
from application.services import analyze_ping_result


class AsyncPingTableUseCase:
    def __init__(
        self,
        on_result,
        max_concurrent: int = 50,
        timeout_ms: int = 1000,
    ) -> None:
        self._executor = AsyncPingExecutor()
        self._on_result = on_result
        self._timeout_ms = timeout_ms
        self._sem = asyncio.Semaphore(max_concurrent)
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    async def run(self, ip_values: list[str]) -> None:
        tasks = []
        for idx, value in enumerate(ip_values):
            tasks.append(asyncio.create_task(self._handle_one(idx, value)))
        await asyncio.gather(*tasks)

    async def _handle_one(self, row: int, value: str) -> None:
        if self._cancelled:
            return

        if not value:
            self._on_result(row, PingStatus.MISSING)
            return

        try:
            ip = IPAddress(value)
        except ValueError:
            self._on_result(row, PingStatus.ERROR)
            return

        async with self._sem:
            if self._cancelled:
                return

            # В процессе
            self._on_result(row, PingStatus.PENDING)

            exit_code, output = await self._executor.ping_with_output(
                ip=ip.value,
                count=1,
                timeout_ms=self._timeout_ms,
            )

            status = analyze_ping_result(
                    stdout = "\n".join(output),
                    exit_code = exit_code,
                    )

            self._on_result(row, status)
