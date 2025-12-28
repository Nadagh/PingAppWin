# presentation/qt/views/network_scan/network_scan_tab.py

from PySide6.QtWidgets import QWidget, QVBoxLayout

from .input_panel import InputPanel
from .controls_panel import ControlsPanel
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

        self.controls.start_btn.clicked.connect(self._on_start_clicked)
        self.controls.stop_btn.clicked.connect(self._on_stop_clicked)

    def _on_start_clicked(self) -> None:
        """
        TODO:
        Подключить NetworkScanPresenter.
        Здесь должно быть:
        - разбор ввода диапазонов
        - запуск use case сканирования
        - блокировка/разблокировка кнопок
        - инициализация прогресса
        """
        self.tables.clear()
        self.progress.reset()

    def _on_stop_clicked(self) -> None:
        """
        TODO:
        Остановить текущий процесс сканирования через Presenter.
        """
        pass
