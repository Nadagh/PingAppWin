# presentation/qt/views/console/output_panel.py

from PySide6.QtGui import QTextCursor, QTextCharFormat
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

from application.services import ConsoleLineType
from presentation.qt.mappers.console_line_mapper import map_console_line



class OutputPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet(
                """
                            QTextEdit {
                                background-color: #1e1e1e;
                                color: #d4d4d4;
                                font-family: Consolas, "Courier New", monospace;
                                font-size: 16pt;
                            }
                        """
                )

        layout = QVBoxLayout(self)
        layout.addWidget(self.console)


    def clear(self) -> None:
        self.console.clear()


    def append_line(self, text: str, line_type: ConsoleLineType) -> None:
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.End)

        fmt = map_console_line(line_type)

        cursor.setCharFormat(fmt)
        cursor.insertText(text + "\n")
        self.console.setTextCursor(cursor)

