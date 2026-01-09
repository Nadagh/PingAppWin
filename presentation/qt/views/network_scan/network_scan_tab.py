# presentation/qt/views/network_scan/network_scan_tab.py

from PySide6.QtWidgets import QWidget, QVBoxLayout

from presentation.qt.presenters import NetworkScanPresenter
from .controls_panel import ControlsPanel
from .input_panel import InputPanel
from .progress_panel import ProgressPanel
from .tables_panel import TablesPanel


class NetworkScanTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.input_panel = InputPanel()
        self.controls = ControlsPanel()
        self.progress = ProgressPanel()
        self.tables = TablesPanel()

        layout = QVBoxLayout(self)
        layout.addWidget(self.input_panel)
        layout.addWidget(self.controls)
        layout.addWidget(self.progress)
        layout.addWidget(self.tables, 1)

        self.presenter = NetworkScanPresenter(self)

        self.controls.start_btn.clicked.connect(self.presenter.on_start_clicked)
        self.controls.stop_btn.clicked.connect(self.presenter.on_stop_clicked)
