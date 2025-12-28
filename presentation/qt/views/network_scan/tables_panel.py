# presentation/qt/views/network_scan/tables_panel.py

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,
    QTableWidget, QHeaderView
)


class TablesPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.success = QTableWidget(0, 1)
        self.success.setHorizontalHeaderLabels(["Успешно"])
        self.success.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.fail = QTableWidget(0, 1)
        self.fail.setHorizontalHeaderLabels(["Нет ответа"])
        self.fail.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QHBoxLayout(self)
        layout.addWidget(self.success)
        layout.addWidget(self.fail)

    def clear(self) -> None:
        self.success.setRowCount(0)
        self.fail.setRowCount(0)
