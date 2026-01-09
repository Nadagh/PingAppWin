from PySide6.QtGui import QColor
from domain import PingResultStatus


COLOR_SUCCESS = QColor("#d1e7dd")
COLOR_ERROR = QColor("#f8d7da")
COLOR_IDLE = QColor("#d0d0d0")
COLOR_PENDING = QColor("#fff3cd")


class PingStatusViewModel:
    def __init__(self, text: str, color: QColor) -> None:
        self.text = text
        self.color = color


def map_ping_result_status(status: PingResultStatus) -> PingStatusViewModel:
    match status:
        case PingResultStatus.SUCCESS:
            return PingStatusViewModel("Успешно", COLOR_SUCCESS)

        case PingResultStatus.UNREACHABLE:
            return PingStatusViewModel("Узел недоступен", COLOR_ERROR)

        case PingResultStatus.TIMEOUT:
            return PingStatusViewModel("Время ожидания истекло", COLOR_ERROR)

        case PingResultStatus.HOST_NOT_FOUND:
            return PingStatusViewModel("Хост не найден", COLOR_ERROR)

        case PingResultStatus.INVALID_ADDRESS:
            return PingStatusViewModel("Неверный IP адрес", COLOR_ERROR)

        case PingResultStatus.ERROR:
            return PingStatusViewModel("Ошибка", COLOR_ERROR)

        case PingResultStatus.MISSING_ADDRESS:
            return PingStatusViewModel("IP не указан", COLOR_IDLE)

        case PingResultStatus.PENDING:
            return PingStatusViewModel("В процессе", COLOR_PENDING)

        case _:
            return PingStatusViewModel("Ожидание", COLOR_IDLE)
