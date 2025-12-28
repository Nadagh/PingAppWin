# presentation/qt/views/ping/ping_tab.py

from PySide6.QtWidgets import QWidget, QVBoxLayout

from application.use_cases.ping_table import PingTableUseCase
from .controls_panel import ControlsPanel
from .table_panel import TablePanel
from ...presenters import PingPresenter


class PingTab(QWidget):
    def __init__(self) -> None:
        super().__init__()


        self.controls = ControlsPanel()
        self.table_panel = TablePanel()

        # Presenter
        use_case = PingTableUseCase()
        self.presenter = PingPresenter(self, use_case)

        layout = QVBoxLayout(self)
        layout.addWidget(self.controls)
        layout.addWidget(self.table_panel)

        # UI-связи
        self.controls.add_btn.clicked.connect(self.table_panel.add_row)
        self.controls.remove_btn.clicked.connect(self._remove_selected)
        self.controls.start_btn.clicked.connect(self.presenter.on_start_clicked)

        # минимум одна строка
        self.table_panel.add_row()

    def _remove_selected(self) -> None:
        rows = {index.row() for index in self.table_panel.table.selectedIndexes()}
        self.table_panel.remove_rows(list(rows))
