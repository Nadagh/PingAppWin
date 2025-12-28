# presentation/qt/views/network_scan/progress_panel.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QLabel, QProgressBar, QSizePolicy
)


class ProgressPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setMinimumHeight(40)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.label = QLabel("Прогресс: 0 / 0")

        self.bar = QProgressBar()
        self.bar.setMaximumHeight(20)
        self.bar.setTextVisible(True)
        self.bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.bar.setStyleSheet("""
            QProgressBar {
                border: none;
                text-align: center;
                background-color: #e0e0e0;
            }
            QProgressBar::chunk {
                background-color: #00aa00;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.addWidget(self.label)
        layout.addWidget(self.bar)

    def reset(self) -> None:
        self.label.setText("Прогресс: 0 / 0")
        self.bar.setValue(0)
