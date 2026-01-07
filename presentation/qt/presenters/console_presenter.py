class ConsolePresenter:
    """
    Presenter для ConsoleTab.
    """

    def __init__(self, view, use_case) -> None:
        self.view = view
        self.use_case = use_case

    def on_start_clicked(self) -> None:
        # подготовка UI
        self.view.output.clear()
        self.view.controls.start_btn.setEnabled(False)

        ip = self.view.controls.ip_input.text().strip()
        count = (
            None
            if self.view.controls.infinite_checkbox.isChecked()
            else self.view.controls.count_input.value()
        )

        try:
            self.use_case.start_ping(ip=ip, count=count)
        finally:
            # синхронный ping → разблокируем сразу после завершения
            self.view.controls.start_btn.setEnabled(True)
