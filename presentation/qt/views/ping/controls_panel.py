# presentation/qt/views/ping/controls_panel.py

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,
    QLabel, QSpinBox, QPushButton
)


class ControlsPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        count_label = QLabel("Количество запросов:")
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 10000)
        self.count_input.setValue(4)

        self.add_btn = QPushButton("Добавить")
        self.remove_btn = QPushButton("Удалить")
        self.start_btn = QPushButton("Ping")

        layout = QHBoxLayout(self)
        layout.addWidget(count_label)
        layout.addWidget(self.count_input)
        layout.addSpacing(20)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.remove_btn)
        layout.addStretch()
        layout.addWidget(self.start_btn)
