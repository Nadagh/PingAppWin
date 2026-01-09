# presentation/qt/views/network_scan/controls_panel.py

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,
    QLabel, QSpinBox, QPushButton,
    )

from presentation.qt.strings import BTN_SCAN_START, BTN_SCAN_STOP, BTN_ADAPTERS, LABEL_MAX_PARALLEL, LABEL_COUNT


class ControlsPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.count_input = QSpinBox()
        self.count_input.setRange(1, 10)
        self.count_input.setValue(1)

        self.max_parallel_input = QSpinBox()
        self.max_parallel_input.setRange(1, 300)
        self.max_parallel_input.setValue(100)

        self.start_btn = QPushButton(BTN_SCAN_START)
        self.stop_btn = QPushButton(BTN_SCAN_STOP)
        self.stop_btn.setEnabled(False)

        self.adapters_btn = QPushButton(BTN_ADAPTERS)

        layout = QHBoxLayout(self)
        layout.addWidget(QLabel(LABEL_COUNT))
        layout.addWidget(self.count_input)
        layout.addWidget(QLabel(LABEL_MAX_PARALLEL))
        layout.addWidget(self.max_parallel_input)
        layout.addStretch()
        layout.addWidget(self.adapters_btn)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
