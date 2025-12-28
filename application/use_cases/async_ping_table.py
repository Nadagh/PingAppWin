import asyncio
from typing import Callable

from domain import IPAddress, PingStatus
from domain.services import status_from_exit_code
from infrastructure import AsyncPingExecutor


ResultCallback = Callable[[int, PingStatus], None]


class AsyncPingTableUseCase:
    """
    Асинхронный use case для PingTab.
    """

    def __init__(self, on_result: ResultCallback, max_concurrent: int = 50) -> None:
        self._executor = AsyncPingExecutor()
        self._on_result = on_result
        self._sem = asyncio.Semaphore(max_concurrent)

    async def run(self, ip_values: list[str]) -> None:
        tasks = []
        for idx, value in enumerate(ip_values):
            tasks.append(asyncio.create_task(self._handle_one(idx, value)))
        await asyncio.gather(*tasks)

    async def _handle_one(self, row: int, value: str) -> None:
        if not value:
            self._on_result(row, PingStatus.MISSING)
            return

        try:
            ip = IPAddress(value)
        except ValueError:
            self._on_result(row, PingStatus.ERROR)
            return

        async with self._sem:
            exit_code = await self._executor.ping(ip.value, count=1)
            status = status_from_exit_code(exit_code)
            self._on_result(row, status)
