# presentation/qt/views/ping/controls_panel.py

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,
    QLabel, QSpinBox, QPushButton
)


class ControlsPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        count_label = QLabel("Запросов:")
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 10000)
        self.count_input.setValue(4)

        self.add_btn = QPushButton("Добавить")
        self.remove_btn = QPushButton("Удалить")
        self.start_btn = QPushButton("Ping")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)

        self.parallel_input = QSpinBox()
        self.parallel_input.setRange(1, 300)
        self.parallel_input.setValue(50)

        timeout_label = QLabel("Таймаут (мс):")
        self.timeout_input = QSpinBox()
        self.timeout_input.setRange(100, 10000)
        self.timeout_input.setValue(1000)
        self.timeout_input.setSingleStep(100)

        layout = QHBoxLayout(self)
        layout.addWidget(count_label)
        layout.addWidget(self.count_input)
        layout.addSpacing(20)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.remove_btn)
        layout.addWidget(QLabel("Параллельно:"))
        layout.addWidget(self.parallel_input)
        layout.addSpacing(10)
        layout.addWidget(timeout_label)
        layout.addWidget(self.timeout_input)
        layout.addStretch()
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)

