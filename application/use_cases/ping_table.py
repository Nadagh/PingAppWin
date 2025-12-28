# application/use_cases/ping_table.py

from domain import IPAddress, PingStatus


class PingTableUseCase:
    """
    Application-layer use case для PingTab.
    Связывает Presenter ↔ Domain.
    """

    def __init__(self) -> None:
        pass

    def prepare_ping(self, ip_values: list[str]) -> list[tuple[str, PingStatus]]:
        """
        Подготавливает ping:
        - валидирует IP
        - возвращает доменные статусы

        TODO:
        Подключить Infrastructure для реального ping.
        """
        results: list[tuple[str, PingStatus]] = []

        for value in ip_values:
            if not value:
                results.append((value, PingStatus.MISSING))
                continue

            try:
                ip = IPAddress(value)
                results.append((ip.value, PingStatus.PENDING))
            except ValueError:
                results.append((value, PingStatus.ERROR))

        return results
