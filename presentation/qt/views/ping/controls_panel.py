# presentation/qt/views/ping/controls_panel.py

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,
    QLabel, QSpinBox, QPushButton
)

from presentation.qt.strings import BTN_REMOVE_ROW, BTN_ADD_ROW
from presentation.qt.strings.common import LABEL_COUNT, BTN_STOP, BTN_START, LABEL_TIMEOUT
from presentation.qt.strings.ping_tab import LABEL_PARALLEL


class ControlsPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        count_label = QLabel(LABEL_COUNT)
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 10000)
        self.count_input.setValue(4)

        self.add_btn = QPushButton(BTN_ADD_ROW)
        self.remove_btn = QPushButton(BTN_REMOVE_ROW)
        self.start_btn = QPushButton(BTN_START)
        self.stop_btn = QPushButton(BTN_STOP)
        self.stop_btn.setEnabled(False)

        self.parallel_input = QSpinBox()
        self.parallel_input.setRange(1, 300)
        self.parallel_input.setValue(50)

        timeout_label = QLabel(LABEL_TIMEOUT)
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
        layout.addWidget(QLabel(LABEL_PARALLEL))
        layout.addWidget(self.parallel_input)
        layout.addSpacing(10)
        layout.addWidget(timeout_label)
        layout.addWidget(self.timeout_input)
        layout.addStretch()
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)

