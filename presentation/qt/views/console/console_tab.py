# presentation/qt/views/console/console_tab.py

from PySide6.QtWidgets import QWidget, QVBoxLayout

from application.use_cases.console_ping import ConsolePingUseCase
from presentation.qt.presenters import ConsolePresenter
from .controls_panel import ControlsPanel
from .output_panel import OutputPanel


class ConsoleTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.controls = ControlsPanel()
        self.output = OutputPanel()

        layout = QVBoxLayout(self)
        layout.addWidget(self.controls)
        layout.addWidget(self.output)

        # UI-only поведение
        self.controls.infinite_checkbox.stateChanged.connect(
                self._on_infinite_changed
                )

        use_case = ConsolePingUseCase(self.output.append_line)
        self.presenter = ConsolePresenter(self, use_case)

        self.controls.start_btn.clicked.connect(self.presenter.on_start_clicked)
        self.controls.stop_btn.clicked.connect(self.presenter.on_stop_clicked)


    def _on_infinite_changed(self, state: int) -> None:
        self.controls.count_input.setEnabled(not bool(state))
