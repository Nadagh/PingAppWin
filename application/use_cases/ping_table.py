from typing import List, Tuple

from domain import IPAddress
from domain.value_objects.ping_result_status import PingResultStatus


class PingExecutorPort:
    def ping(self, ip: str) -> int:
        raise NotImplementedError


class PingTableUseCase:
    def prepare_ping(
        self,
        ip_values: List[str],
    ) -> List[Tuple[str, PingResultStatus]]:
        results: List[Tuple[str, PingResultStatus]] = []

        for raw_ip in ip_values:
            # --- пусто ---
            if not raw_ip.strip():
                results.append((raw_ip, PingResultStatus.MISSING_ADDRESS))
                continue

            # --- валидация ---
            try:
                IPAddress(raw_ip)
            except ValueError:
                results.append((raw_ip, PingResultStatus.INVALID_ADDRESS))
                continue

            executor = PingExecutorPort()

            # --- выполнение ---
            try:
                exit_code = executor.ping(raw_ip, count=1)

            except Exception:
                results.append((raw_ip, PingResultStatus.ERROR))
                continue

            # --- интерпретация ---
            if exit_code == 0:
                status = PingResultStatus.SUCCESS
            else:
                status = PingResultStatus.UNREACHABLE

            results.append((raw_ip, status))

        return results
