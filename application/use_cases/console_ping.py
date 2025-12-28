# application/use_cases/console_ping.py

class ConsolePingUseCase:
    """
    Application-layer use case для консольного ping.
    """

    def __init__(self, output_callback) -> None:
        self.output_callback = output_callback

    def start_ping(self, ip: str, count: int | None) -> None:
        """
        TODO:
        Подключить Domain + Infrastructure (реальный ping).
        """
        if not ip:
            self.output_callback("IP адрес не задан")
            return

        self.output_callback(f"Запуск ping для {ip}")
        if count is None:
            self.output_callback("Режим: бесконечный")
        else:
            self.output_callback(f"Количество пакетов: {count}")
