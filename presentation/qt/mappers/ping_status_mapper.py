# presentation/qt/mappers/ping_status_mapper.py

from PySide6.QtGui import QColor

from domain import PingStatus


COLOR_SUCCESS = QColor("#d1e7dd")  # мягкий зелёный
COLOR_ERROR = QColor("#f8d7da")  # мягкий красный
COLOR_IDLE = QColor("#d0d0d0")  # серый (ожидание)
COLOR_PENDING = QColor("#fff3cd")  # мягкий жёлтый



class PingStatusViewModel:
    """
    View-model для отображения статуса ping в таблице.
    """


    def __init__(self, text: str, color: QColor) -> None:
        self.text = text
        self.color = color


def map_ping_status(status: PingStatus) -> PingStatusViewModel:
    if status == PingStatus.SUCCESS:
        return PingStatusViewModel("Успешно", COLOR_SUCCESS)

    if status == PingStatus.FAILURE:
        return PingStatusViewModel("Нет ответа", COLOR_ERROR)

    if status in (PingStatus.ERROR, PingStatus.MISSING):
        return PingStatusViewModel(
            "Не указан IP" if status == PingStatus.MISSING else "Ошибка IP",
            COLOR_ERROR,
        )

    if status == PingStatus.PENDING:
        return PingStatusViewModel("В процессе", COLOR_PENDING)

    return PingStatusViewModel("Ожидание", COLOR_IDLE)

