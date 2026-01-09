import threading
from unittest.mock import Mock

import pytest

from domain import PingStatus
from presentation.qt.presenters.ping_presenter import PingPresenter
from presentation.qt.mappers.ping_status_mapper import PingStatusViewModel


# =========================
# Fakes (минимальный контракт)
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
        # rows: list[str]
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

def test_start_click_collects_ips_and_starts_use_case(monkeypatch):
    view = FakeView(["8.8.8.8", "1.1.1.1"])
    presenter = PingPresenter(view, None)

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

    fake_thread.start.assert_called_once()
    view.controls.start_btn.setEnabled.assert_called_with(False)
    view.controls.stop_btn.setEnabled.assert_called_with(True)


def test_start_click_with_empty_values_does_not_crash(monkeypatch):
    view = FakeView(["", "   "])
    presenter = PingPresenter(view, None)

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

    fake_thread.start.assert_called_once()


def test_on_async_result_updates_correct_row(monkeypatch):
    view = FakeView(["8.8.8.8"])
    presenter = PingPresenter(view, None)

    fake_vm = PingStatusViewModel("Успешно", object())

    monkeypatch.setattr(
        "presentation.qt.presenters.ping_presenter.map_ping_status",
        Mock(return_value=fake_vm),
    )

    presenter._on_async_result(0, PingStatus.SUCCESS)

    item = view.table_panel.table.item(0, 1)
    assert item.text() == "Успешно"
    assert item.background is fake_vm.color


def test_on_async_result_ignored_if_item_missing(monkeypatch):
    view = FakeView(["8.8.8.8"])
    presenter = PingPresenter(view, None)

    # эмулируем отсутствие status item
    view.table_panel.table._status_items[0] = None

    presenter._on_async_result(0, PingStatus.SUCCESS)  # не должно упасть


def test_stop_click_cancels_use_case_and_resets_buttons():
    view = FakeView(["8.8.8.8"])
    presenter = PingPresenter(view, None)

    presenter._use_case = Mock()

    presenter.on_stop_clicked()

    presenter._use_case.cancel.assert_called_once()
    view.controls.start_btn.setEnabled.assert_called_with(True)
    view.controls.stop_btn.setEnabled.assert_called_with(False)
