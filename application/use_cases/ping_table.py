# application/use_cases/ping_table.py


from domain import IPAddress, PingStatus
from domain.services import status_from_exit_code
from infrastructure import PingExecutor


class PingTableUseCase:
    """
    Application-layer use case для PingTab.
    Связывает Presenter ↔ Domain.
    """


    def __init__(self) -> None:
        self.executor = PingExecutor()


    def prepare_ping(self, ip_values: list[str]) -> list[tuple[str, PingStatus]]:
        results = []

        for value in ip_values:
            if not value:
                results.append((value, PingStatus.MISSING))
                continue

            try:
                ip = IPAddress(value)
            except ValueError:
                results.append((value, PingStatus.ERROR))
                continue

            try:
                exit_code = self.executor.ping(ip.value, count = 1)
            except Exception:
                results.append((value, PingStatus.ERROR))
                continue

            status = status_from_exit_code(exit_code)
            results.append((ip.value, status))

        return results
