# presentation/qt/mappers/ping_status_mapper.py

from PySide6.QtGui import QColor

from domain import PingStatus


COLOR_SUCCESS = QColor("#d1e7dd")  # мягкий зелёный
COLOR_WARNING = QColor("#fff3cd")  # мягкий жёлтый
COLOR_ERROR = QColor("#f8d7da")  # мягкий красный
COLOR_IDLE = QColor("#d0d0d0")  # серый (ожидание)


class PingStatusViewModel:
    """
    View-model для отображения статуса ping в таблице.
    """


    def __init__(self, text: str, color: QColor) -> None:
        self.text = text
        self.color = color


def map_ping_status(status: PingStatus) -> PingStatusViewModel:
    if status == PingStatus.SUCCESS:
        return PingStatusViewModel(
                text = "Успешно",
                color = COLOR_SUCCESS,
                )

    if status == PingStatus.FAILURE:
        return PingStatusViewModel(
                text = "Нет ответа",
                color = COLOR_ERROR,
                )

    if status in (PingStatus.ERROR, PingStatus.MISSING):
        return PingStatusViewModel(
                text = "Ошибка IP" if status == PingStatus.ERROR else "Не указан IP",
                color = COLOR_ERROR,
                )

    return PingStatusViewModel(
            text = "Ожидание",
            color = COLOR_IDLE,
            )
