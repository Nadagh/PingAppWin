# presentation/qt/views/network_scan/input_panel.py

from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout

from presentation.qt.strings import SCAN_INPUT_PLACEHOLDER


class InputPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setMaximumHeight(60)

        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText(SCAN_INPUT_PLACEHOLDER)

        layout = QVBoxLayout(self)
        layout.addWidget(self.input_edit)
