# presentation/qt/views/console/controls_panel.py

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,
    QLabel, QLineEdit, QSpinBox,
    QPushButton, QCheckBox
)


class ControlsPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        ip_label = QLabel("IP адрес:")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("8.8.8.8")

        count_label = QLabel("Запросов:")
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 10000)
        self.count_input.setValue(4)

        self.infinite_checkbox = QCheckBox("Бесконечный ping")

        self.start_btn = QPushButton("Ping")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)

        timeout_label = QLabel("Таймаут (мс):")
        self.timeout_input = QSpinBox()
        self.timeout_input.setRange(100, 10000)
        self.timeout_input.setValue(1000)
        self.timeout_input.setSingleStep(100)

        layout = QHBoxLayout(self)
        layout.addWidget(ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(count_label)
        layout.addWidget(self.count_input)
        layout.addWidget(self.infinite_checkbox)
        layout.addWidget(timeout_label)
        layout.addWidget(self.timeout_input)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
