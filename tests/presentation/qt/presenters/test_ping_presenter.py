# tests/presentation/qt/presenters/test_ping_presenter.py

from unittest.mock import Mock
import pytest

from presentation.qt.presenters.ping_presenter import PingPresenter
from domain.value_objects.ping_result_status import PingResultStatus


# =========================
# Fakes (минимальный контракт UI)
# =========================

class FakeItem:
    def __init__(self, text=""):
        self._text = text
        self.background = None

    def text(self):
        return self._text

    def setText(self, text):
        self._text = text

    def setBackground(self, color):
        self.background = color


class FakeTable:
    def __init__(self, rows):
        self._rows = rows
        self._status_items = [FakeItem() for _ in rows]

    def rowCount(self):
        return len(self._rows)

    def item(self, row, column):
        if column == 0:
            return FakeItem(self._rows[row])
        if column == 1:
            return self._status_items[row]
        return None


class FakeControls:
    def __init__(self):
        self.start_btn = Mock()
        self.stop_btn = Mock()
        self.parallel_input = Mock(value=Mock(return_value=10))
        self.timeout_input = Mock(value=Mock(return_value=1000))


class FakeTablePanel:
    def __init__(self, rows):
        self.table = FakeTable(rows)


class FakeView:
    def __init__(self, rows):
        self.controls = FakeControls()
        self.table_panel = FakeTablePanel(rows)


# =========================
# Tests
# =========================

def test_start_click_disables_start_and_enables_stop(monkeypatch):
    view = FakeView(["8.8.8.8"])
    presenter = PingPresenter(view)

    fake_use_case = Mock()
    fake_thread = Mock()

    monkeypatch.setattr(
        "presentation.qt.presenters.ping_presenter.AsyncPingTableUseCase",
        Mock(return_value=fake_use_case),
    )
    monkeypatch.setattr(
        "presentation.qt.presenters.ping_presenter.threading.Thread",
        Mock(return_value=fake_thread),
    )

    presenter.on_start_clicked()

    view.controls.start_btn.setEnabled.assert_called_with(False)
    view.controls.stop_btn.setEnabled.assert_called_with(True)
    fake_thread.start.assert_called_once()


def test_collect_ip_values():
    view = FakeView(["8.8.8.8", "1.1.1.1"])
    presenter = PingPresenter(view)

    ips = presenter._collect_ip_values()

    assert ips == ["8.8.8.8", "1.1.1.1"]


def test_on_async_result_updates_correct_row(monkeypatch):
    view = FakeView(["8.8.8.8"])
    presenter = PingPresenter(view)

    fake_vm = Mock()
    fake_vm.text = "Успешно"
    fake_vm.color = object()

    monkeypatch.setattr(
        "presentation.qt.presenters.ping_presenter.map_ping_result_status",
        Mock(return_value=fake_vm),
    )

    presenter._on_async_result(0, PingResultStatus.SUCCESS)

    item = view.table_panel.table.item(0, 1)
    assert item.text() == "Успешно"
    assert item.background is fake_vm.color


def test_on_async_result_ignored_if_item_missing():
    view = FakeView(["8.8.8.8"])
    presenter = PingPresenter(view)

    # статусная ячейка отсутствует
    view.table_panel.table._status_items[0] = None

    # не должно падать
    presenter._on_async_result(0, PingResultStatus.SUCCESS)


def test_stop_click_cancels_use_case_and_resets_buttons():
    view = FakeView(["8.8.8.8"])
    presenter = PingPresenter(view)

    presenter._use_case = Mock()

    presenter.on_stop_clicked()

    presenter._use_case.cancel.assert_called_once()
    view.controls.start_btn.setEnabled.assert_called_with(True)
    view.controls.stop_btn.setEnabled.assert_called_with(False)
