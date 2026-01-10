# application/use_cases/network_scan_use_case.py
import asyncio

from domain.entities.ip_range_set import IPRangeSet


class NetworkScanUseCase:
    def __init__(self, ping_executor) -> None:
        self._executor = ping_executor
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    async def execute(
        self,
        raw_ranges: str,
        count: int,
        max_parallel: int,
        on_progress,
        on_result,
    ) -> None:
        if not raw_ranges or not raw_ranges.strip():
            on_progress(0, 0)
            return

        ranges = IPRangeSet(raw_ranges)
        ips = [ip.value for ip in ranges.expand()]

        total = len(ips)
        done = 0

        semaphore = asyncio.Semaphore(max_parallel)

        async def worker(ip: str):
            nonlocal done

            if self._cancelled:
                return

            async with semaphore:
                if self._cancelled:
                    return

                try:
                    alive = await self._executor.ping(ip, count)
                except Exception:
                    alive = False

                if self._cancelled:
                    return

                done += 1
                on_result(ip, alive)
                on_progress(done, total)

        await asyncio.gather(*(worker(ip) for ip in ips))
