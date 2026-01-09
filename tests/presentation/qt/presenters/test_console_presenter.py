import threading
from unittest.mock import Mock, patch

import pytest

from presentation.qt.presenters.console_presenter import ConsolePresenter
from application.services.console_line_type import ConsoleLineType


@pytest.fixture
def view():
    view = Mock()

    # output
    view.output.clear = Mock()
    view.output.append_line = Mock()

    # controls
    view.controls.start_btn.setEnabled = Mock()
    view.controls.stop_btn.setEnabled = Mock()

    view.controls.ip_input.text.return_value = "8.8.8.8"
    view.controls.count_input.value.return_value = 4
    view.controls.timeout_input.value.return_value = 1000
    view.controls.infinite_checkbox.isChecked.return_value = False

    return view


@pytest.fixture
def use_case():
    uc = Mock()
    uc.start_ping = Mock()
    uc.stop = Mock()
    return uc


def test_start_click_clears_output_and_starts_thread(view, use_case):
    presenter = ConsolePresenter(view, use_case)

    with patch.object(threading, "Thread") as thread_mock:
        presenter.on_start_clicked()

        # UI
        view.output.clear.assert_called_once()
        view.controls.start_btn.setEnabled.assert_called_with(False)
        view.controls.stop_btn.setEnabled.assert_called_with(True)

        # Thread creation
        thread_mock.assert_called_once()
        kwargs = thread_mock.call_args.kwargs
        assert kwargs["daemon"] is True


def test_run_calls_use_case_with_correct_arguments(view, use_case):
    presenter = ConsolePresenter(view, use_case)

    presenter._run("8.8.8.8")

    use_case.start_ping.assert_called_once_with(
        ip="8.8.8.8",
        count=4,
        timeout_ms=1000,
    )

    view.controls.start_btn.setEnabled.assert_called_with(True)
    view.controls.stop_btn.setEnabled.assert_called_with(False)


def test_infinite_checkbox_passes_none_as_count(view, use_case):
    view.controls.infinite_checkbox.isChecked.return_value = True

    presenter = ConsolePresenter(view, use_case)
    presenter._run("1.1.1.1")

    use_case.start_ping.assert_called_once_with(
        ip="1.1.1.1",
        count=None,
        timeout_ms=1000,
    )


def test_stop_click_calls_use_case_stop_and_resets_buttons(view, use_case):
    presenter = ConsolePresenter(view, use_case)

    presenter.on_stop_clicked()

    use_case.stop.assert_called_once()
    view.controls.start_btn.setEnabled.assert_called_with(True)
    view.controls.stop_btn.setEnabled.assert_called_with(False)


def test_on_output_classifies_and_appends_line(view, use_case):
    presenter = ConsolePresenter(view, use_case)

    with patch(
        "presentation.qt.presenters.console_presenter.classify_console_line",
        return_value=ConsoleLineType.ERROR,
    ) as classify_mock:
        presenter.on_output("Request timed out.")

        classify_mock.assert_called_once_with("Request timed out.")
        view.output.append_line.assert_called_once_with(
            "Request timed out.",
            ConsoleLineType.ERROR,
        )
