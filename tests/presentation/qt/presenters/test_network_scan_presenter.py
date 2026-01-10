from unittest.mock import Mock

from presentation.qt.presenters import NetworkScanPresenter


def test_start_click_runs_use_case(monkeypatch):
    view = Mock()

    view.input_panel.input_edit.text.return_value = "10.0.0.1-2"
    view.controls.count_input.value.return_value = 1
    view.controls.max_parallel_input.value.return_value = 10

    view.tables.clear = Mock()
    view.progress.reset = Mock()

    view.controls.start_btn.setEnabled = Mock()
    view.controls.stop_btn.setEnabled = Mock()

    fake_use_case = Mock()
    monkeypatch.setattr(
        "presentation.qt.presenters.network_scan_presenter.NetworkScanUseCase",
        Mock(return_value=fake_use_case),
    )

    presenter = NetworkScanPresenter(view)
    presenter.on_start_clicked()

    fake_use_case.execute.assert_called_once()

def test_on_result_routes_ip_to_correct_table():
    view = Mock()

    view.tables.success.insertRow = Mock()
    view.tables.success.setItem = Mock()

    view.tables.fail.insertRow = Mock()
    view.tables.fail.setItem = Mock()

    presenter = NetworkScanPresenter(view)

    presenter._on_result("10.0.0.1", True)
    presenter._on_result("10.0.0.2", False)

    assert view.tables.success.insertRow.called
    assert view.tables.fail.insertRow.called

def test_on_progress_updates_progress_panel():
    view = Mock()

    view.progress.bar.setMaximum = Mock()
    view.progress.bar.setValue = Mock()
    view.progress.label.setText = Mock()

    presenter = NetworkScanPresenter(view)

    presenter._on_progress(3, 10)

    view.progress.bar.setMaximum.assert_called_with(10)
    view.progress.bar.setValue.assert_called_with(3)
    view.progress.label.setText.assert_called_with("Прогресс: 3 / 10")

