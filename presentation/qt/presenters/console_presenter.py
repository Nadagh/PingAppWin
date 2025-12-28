# presentation/qt/presenters/console_presenter.py

class ConsolePresenter:
    """
    Presenter для ConsoleTab.
    """

    def __init__(self, view, use_case) -> None:
        self.view = view
        self.use_case = use_case

    def on_start_clicked(self) -> None:
        ip = self.view.controls.ip_input.text().strip()
        count = (
            None
            if self.view.controls.infinite_checkbox.isChecked()
            else self.view.controls.count_input.value()
        )

        self.use_case.start_ping(ip=ip, count=count)

    def on_output(self, line: str) -> None:
        self.view.output.append_line(line)
