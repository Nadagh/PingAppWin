import asyncio
import threading
from unittest.mock import Mock

from presentation.qt.presenters.network_scan_presenter import NetworkScanPresenter
from application.use_cases.network_scan_use_case import NetworkScanUseCase


class FakePingExecutor:
    """
    Реальный async executor-заглушка.
    """

    def __init__(self, alive_map: dict[str, bool]) -> None:
        self._alive_map = alive_map

    async def ping(self, ip: str, count: int) -> bool:
        await asyncio.sleep(0)
        return self._alive_map.get(ip, False)


def test_network_scan_presenter_with_real_use_case(monkeypatch):
    # =========================
    # View mock
    # =========================
    view = Mock()

    view.input_panel.input_edit.text.return_value = "10.0.0.1-3"
    view.controls.count_input.value.return_value = 1
    view.controls.max_parallel_input.value.return_value = 1

    view.tables.clear = Mock()

    view.tables.success.rowCount.return_value = 0
    view.tables.success.insertRow = Mock()
    view.tables.success.setItem = Mock()

    view.tables.fail.rowCount.return_value = 0
    view.tables.fail.insertRow = Mock()
    view.tables.fail.setItem = Mock()

    view.progress.reset = Mock()
    view.progress.bar.setMaximum = Mock()
    view.progress.bar.setValue = Mock()
    view.progress.label.setText = Mock()

    view.controls.start_btn.setEnabled = Mock()
    view.controls.stop_btn.setEnabled = Mock()

    # =========================
    # Реальный UseCase
    # =========================
    alive_map = {
        "10.0.0.1": True,
        "10.0.0.2": False,
        "10.0.0.3": True,
    }

    real_use_case = NetworkScanUseCase(
        ping_executor=FakePingExecutor(alive_map)
    )

    # Подменяем конструктор UseCase в Presenter
    monkeypatch.setattr(
        "presentation.qt.presenters.network_scan_presenter.NetworkScanUseCase",
        lambda ping_executor=None: real_use_case,
    )

    # =========================
    # Подмена threading.Thread
    # =========================
    def fake_thread(*, target, daemon):
        class _T:
            def start(self):
                target()

        return _T()

    monkeypatch.setattr(threading, "Thread", fake_thread)

    # =========================
    # Запуск
    # =========================
    presenter = NetworkScanPresenter(view)
    presenter.on_start_clicked()

    # =========================
    # Проверки
    # =========================

    # success: 10.0.0.1, 10.0.0.3
    assert view.tables.success.insertRow.call_count == 2
    assert view.tables.success.setItem.call_count == 2

    # fail: 10.0.0.2
    assert view.tables.fail.insertRow.call_count == 1
    assert view.tables.fail.setItem.call_count == 1

    # progress дошёл до конца
    view.progress.bar.setMaximum.assert_called_with(3)
    view.progress.bar.setValue.assert_called_with(3)
    view.progress.label.setText.assert_called_with("Прогресс: 3 / 3")

    # UI вернулся в idle
    view.controls.start_btn.setEnabled.assert_called_with(True)
    view.controls.stop_btn.setEnabled.assert_called_with(False)
