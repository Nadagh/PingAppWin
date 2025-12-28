# presentation/qt/main_window.py

from PySide6.QtWidgets import QMainWindow, QTabWidget

from presentation.qt.views.ping import PingTab


from presentation.qt.views.console import ConsoleTab
from presentation.qt.views.network_scan import NetworkScanTab


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("MyPing")
        self.setFixedSize(800, 500)

        tabs = QTabWidget()
        tabs.addTab(PingTab(), "Ping")
        tabs.addTab(ConsoleTab(), "Console")
        tabs.addTab(NetworkScanTab(), "Network Scan")

        self.setCentralWidget(tabs)
