# presentation/qt/views/network_scan/input_panel.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit

from presentation.qt.strings import SCAN_INPUT_PLACEHOLDER


class InputPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText(SCAN_INPUT_PLACEHOLDER)
        self.input_edit.setClearButtonEnabled(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.input_edit)
