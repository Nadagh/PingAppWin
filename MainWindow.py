from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    )

from ConsoleTab import ConsoleTab
from NetworkScanTab import NetworkScanTab
from PingTab import PingTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyPing")
        # self.resize(800, 500)

        # Фиксируем размер окна
        self.setFixedSize(800, 500)

        tabs = QTabWidget()

        # --- Вкладка 1 ---
        tabs.addTab(PingTab(), "Ping")

        # --- Вкладка 2 ---
        tabs.addTab(ConsoleTab(), "Console")

        # --- Вкладка 3 ---

        tabs.addTab(NetworkScanTab(), "Network Scan")

        self.setCentralWidget(tabs)
