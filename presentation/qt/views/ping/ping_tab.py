# presentation/qt/views/ping/ping_tab.py

from PySide6.QtWidgets import QWidget, QVBoxLayout

from .controls_panel import ControlsPanel
from .table_panel import TablePanel


class PingTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.controls = ControlsPanel()
        self.table_panel = TablePanel()

        layout = QVBoxLayout(self)
        layout.addWidget(self.controls)
        layout.addWidget(self.table_panel)

        # UI-связи
        self.controls.add_btn.clicked.connect(self.table_panel.add_row)
        self.controls.remove_btn.clicked.connect(self._remove_selected)

        # минимум одна строка
        self.table_panel.add_row()

    def _remove_selected(self) -> None:
        rows = {index.row() for index in self.table_panel.table.selectedIndexes()}
        self.table_panel.remove_rows(list(rows))
