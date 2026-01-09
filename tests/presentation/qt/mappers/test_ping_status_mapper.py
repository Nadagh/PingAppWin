# tests/presentation/qt/mappers/test_ping_status_mapper.py

from PySide6.QtGui import QColor
import pytest

from domain.value_objects.ping_result_status import PingResultStatus
from presentation.qt.mappers.ping_status_mapper import (
    map_ping_result_status,
    PingStatusViewModel,
    COLOR_SUCCESS,
    COLOR_ERROR,
    COLOR_IDLE,
    COLOR_PENDING,
)


def test_mapper_returns_view_model():
    vm = map_ping_result_status(PingResultStatus.SUCCESS)

    assert isinstance(vm, PingStatusViewModel)
    assert isinstance(vm.text, str)
    assert isinstance(vm.color, QColor)


@pytest.mark.parametrize(
    "status, expected_text, expected_color",
    [
        # SUCCESS
        (PingResultStatus.SUCCESS, "Успешно", COLOR_SUCCESS),

        # Сетевые ошибки (красные)
        (PingResultStatus.UNREACHABLE, "Узел недоступен", COLOR_ERROR),
        (PingResultStatus.TIMEOUT, "Время ожидания истекло", COLOR_ERROR),
        (PingResultStatus.HOST_NOT_FOUND, "Хост не найден", COLOR_ERROR),

        # Ошибки ввода / инфраструктуры
        (PingResultStatus.INVALID_ADDRESS, "Неверный IP адрес", COLOR_ERROR),
        (PingResultStatus.ERROR, "Ошибка", COLOR_ERROR),

        # Состояния
        (PingResultStatus.MISSING_ADDRESS, "IP не указан", COLOR_IDLE),
        (PingResultStatus.PENDING, "В процессе", COLOR_PENDING),
    ],
)
def test_status_mapping(status, expected_text, expected_color):
    vm = map_ping_result_status(status)

    assert vm.text == expected_text
    assert vm.color == expected_color


def test_unknown_status_falls_back_to_idle():
    class FakeStatus:
        pass

    vm = map_ping_result_status(FakeStatus())  # type: ignore

    assert vm.text == "Ожидание"
    assert vm.color == COLOR_IDLE
