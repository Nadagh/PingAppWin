# presentation/qt/main_window.py

from PySide6.QtWidgets import QMainWindow, QTabWidget

from presentation.qt.strings import APP_TITLE, SCAN_TAB_TITLE
from presentation.qt.strings.console_tab import CONSOLE_TAB_TITLE
from presentation.qt.strings.ping_tab import PING_TAB_TITLE
from presentation.qt.views.console import ConsoleTab
from presentation.qt.views.network_scan import NetworkScanTab
from presentation.qt.views.ping import PingTab


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(APP_TITLE)
        self.setFixedSize(800, 500)

        tabs = QTabWidget()
        tabs.addTab(PingTab(), PING_TAB_TITLE)
        tabs.addTab(ConsoleTab(), CONSOLE_TAB_TITLE)
        tabs.addTab(NetworkScanTab(), SCAN_TAB_TITLE)

        self.setCentralWidget(tabs)
