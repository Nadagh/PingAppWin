# presentation/qt/views/ping/table_panel.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtGui import QColor


class TablePanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["IP адрес", "Статус"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 180)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

    def add_row(self) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(""))

        status = QTableWidgetItem("Ожидание")
        status.setBackground(QColor("#cccccc"))
        self.table.setItem(row, 1, status)

    def remove_rows(self, rows: list[int]) -> None:
        for row in sorted(rows, reverse=True):
            if self.table.rowCount() > 1:
                self.table.removeRow(row)
