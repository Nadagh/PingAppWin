# presentation/qt/views/console/console_tab.py

from PySide6.QtWidgets import QWidget, QVBoxLayout

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
        self.controls.start_btn.clicked.connect(self._on_start_clicked)

    def _on_infinite_changed(self, state: int) -> None:
        self.controls.count_input.setEnabled(not bool(state))

    def _on_start_clicked(self) -> None:
        """
        TODO:
        Подключить ConsolePresenter.
        Здесь должна быть:
        - валидация ввода
        - запуск use case
        - подписка на поток вывода
        """
        self.output.clear()
        self.output.append_line("Ожидание запуска ping...")
