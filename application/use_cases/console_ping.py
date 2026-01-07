from domain import IPAddress
from infrastructure import ConsolePingExecutor


class ConsolePingUseCase:
    def __init__(self, output_callback) -> None:
        self._output = output_callback
        self._executor = ConsolePingExecutor()


    def start_ping(self, ip: str, count: int | None) -> None:
        if not ip:
            self._output("Ошибка: IP адрес не задан")
            return

        try:
            address = IPAddress(ip)
        except ValueError:
            self._output("Ошибка: неверный IP адрес")
            return

        # ВАЖНО: никаких служебных строк
        self._executor.run(
                ip = address.value,
                count = count,
                on_output = self._output,
                )


    def stop(self) -> None:
        self._executor.stop()
