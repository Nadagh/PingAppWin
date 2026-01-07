import threading


class ConsolePresenter:
    def __init__(self, view, use_case) -> None:
        self.view = view
        self.use_case = use_case
        self._thread: threading.Thread | None = None

    def on_start_clicked(self) -> None:
        self.view.output.clear()
        self.view.controls.start_btn.setEnabled(False)

        ip = self.view.controls.ip_input.text().strip()
        count = (
            None
            if self.view.controls.infinite_checkbox.isChecked()
            else self.view.controls.count_input.value()
        )

        self._thread = threading.Thread(
            target=self._run,
            args=(ip, count),
            daemon=True,
        )
        self._thread.start()

    def _run(self, ip: str, count: int | None) -> None:
        try:
            self.use_case.start_ping(ip=ip, count=count)
        finally:
            self.view.controls.start_btn.setEnabled(True)

    def on_stop_clicked(self) -> None:
        self.use_case.stop()
