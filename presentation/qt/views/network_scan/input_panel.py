# presentation/qt/views/network_scan/input_panel.py

from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout


class InputPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setMaximumHeight(60)

        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText(
            "150.102.95.5-100\n"
            "150.102.1-255.25-50\n"
            "150.102.0.0/16\n"
            "150.102.0.0 - 150.102.255.255"
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.input_edit)
