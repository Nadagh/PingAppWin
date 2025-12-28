# presentation/qt/app.py

from PySide6.QtWidgets import QApplication
from presentation.qt.main_window import MainWindow


def run_app() -> None:
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
