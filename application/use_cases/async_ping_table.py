import asyncio
from typing import Callable

from domain import IPAddress
from domain.value_objects.ping_result_status import PingResultStatus
from application.services.ping_result_analyzer import analyze_ping_result
from infrastructure.ping.async_ping_executor import AsyncPingExecutor


class AsyncPingTableUseCase:
    def __init__(
        self,
        on_result: Callable[[int, PingResultStatus], None],
        max_concurrent: int = 5,
        timeout_ms: int = 1000,
    ) -> None:
        self._on_result = on_result
        self._max_concurrent = max_concurrent
        self._timeout_ms = timeout_ms
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    async def run(self, ip_values: list[str]) -> None:
        semaphore = asyncio.Semaphore(self._max_concurrent)

        tasks = [
            asyncio.create_task(
                self._process_one(row, ip, semaphore)
            )
            for row, ip in enumerate(ip_values)
        ]

        await asyncio.gather(*tasks, return_exceptions=True)

    async def _process_one(
        self,
        row: int,
        raw_ip: str,
        semaphore: asyncio.Semaphore,
    ) -> None:
        if self._cancelled:
            return

        if not raw_ip.strip():
            self._on_result(row, PingResultStatus.MISSING_ADDRESS)
            return

        try:
            IPAddress(raw_ip)
        except ValueError:
            self._on_result(row, PingResultStatus.INVALID_ADDRESS)
            return

        self._on_result(row, PingResultStatus.PENDING)

        async with semaphore:
            if self._cancelled:
                return

            executor = AsyncPingExecutor()

            try:
                exit_code, output = await executor.ping_with_output(
                    raw_ip,
                    count=1,
                    timeout_ms=self._timeout_ms,
                )
            except Exception:
                self._on_result(row, PingResultStatus.ERROR)
                return

        stdout = "\n".join(output)
        status = analyze_ping_result(stdout, exit_code)
        self._on_result(row, status)
