from domain import IPAddress
from infrastructure import ConsolePingExecutor


class ConsolePingUseCase:
    """
    Application-layer use case для консольного ping.
    """

    def __init__(self, output_callback) -> None:
        self._output = output_callback
        self._executor = ConsolePingExecutor()

    def start_ping(self, ip: str, count: int | None) -> None:
        if not ip:
            self._output("Ошибка: IP адрес не задан")
            return

        try:
            address = IPAddress(ip)
        except ValueError as exc:
            self._output(str(exc))
            return

        self._output(f"Запуск ping для {address.value}")

        if count is None:
            self._output("Режим: бесконечный")
        else:
            self._output(f"Количество пакетов: {count}")

        self._executor.run(
            ip=address.value,
            count=count,
            on_output=self._output,
        )
