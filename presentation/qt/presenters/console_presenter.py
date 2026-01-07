import threading

from application.services import classify_console_line


class ConsolePresenter:
    def __init__(self, view, use_case) -> None:
        self.view = view
        self.use_case = use_case
        self._thread: threading.Thread | None = None


    def on_start_clicked(self) -> None:
        self.view.output.clear()
        self._set_running(True)

        ip = self.view.controls.ip_input.text().strip()

        self._thread = threading.Thread(
                target = self._run,
                args = (ip,),
                daemon = True,
                )
        self._thread.start()


    def _run(self, ip: str) -> None:
        try:
            count = (
                    None
                    if self.view.controls.infinite_checkbox.isChecked()
                    else self.view.controls.count_input.value()
            )
            timeout = self.view.controls.timeout_input.value()
            self.use_case.start_ping(
                    ip = ip,
                    count = count,
                    timeout_ms = timeout,
                    )

        finally:
            self._set_running(False)


    def on_stop_clicked(self) -> None:
        self.use_case.stop()
        self._set_running(False)


    def _set_running(self, running: bool) -> None:
        self.view.controls.start_btn.setEnabled(not running)
        self.view.controls.stop_btn.setEnabled(running)


    def on_output(self, line: str) -> None:
        line_type = classify_console_line(line)
        self.view.output.append_line(line, line_type)
