# presentation/qt/views/console/output_panel.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor


class OutputPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, "Courier New", monospace;
                font-size: 16pt;
            }
        """)

        layout = QVBoxLayout(self)
        layout.addWidget(self.console)

    def clear(self) -> None:
        self.console.clear()

    def append_line(self, text: str) -> None:
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.End)

        fmt = QTextCharFormat()
        text_l = text.lower()

        if "ttl=" in text_l:
            fmt.setForeground(QColor("#00ff00"))
        elif "timeout" in text_l or "превышен" in text_l or "сбой" in text_l:
            fmt.setForeground(QColor("#f44747"))
        else:
            fmt.setForeground(QColor("#d4d4d4"))

        cursor.setCharFormat(fmt)
        cursor.insertText(text + "\n")
        self.console.setTextCursor(cursor)
