from PySide6.QtCore import QThread
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit,
    QLabel, QSpinBox, QCheckBox
)

from Workers.PingWorker import PingWorker


class ConsoleTab(QWidget):
    def __init__(self):
        super().__init__()

        # --- IP ---
        ip_label = QLabel("IP адрес:")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("например: 8.8.8.8")

        # --- Count ---
        count_label = QLabel("Количество запросов:")
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 10000)
        self.count_input.setValue(4)

        # --- Infinite ---
        self.infinite_checkbox = QCheckBox("Бесконечный ping")
        self.infinite_checkbox.stateChanged.connect(self.on_infinite_changed)

        # --- Button ---
        self.start_btn = QPushButton("Ping")

        # --- Console ---
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

        # --- Layouts ---
        top = QHBoxLayout()
        top.addWidget(ip_label)
        top.addWidget(self.ip_input)
        top.addWidget(count_label)
        top.addWidget(self.count_input)
        top.addWidget(self.infinite_checkbox)
        top.addWidget(self.start_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.console)

        # --- Threading ---
        self.thread: QThread | None = None
        self.worker: PingWorker | None = None

        self.start_btn.clicked.connect(self.on_button_clicked)

    # -------------------------
    # Logic
    # -------------------------

    def on_infinite_changed(self, state: int):
        self.count_input.setEnabled(not state)

    def on_button_clicked(self):
        if self.thread and self.thread.isRunning():
            self.stop_ping()
        else:
            self.start_ping()

    def start_ping(self):
        ip = self.ip_input.text().strip()
        if not ip:
            return

        self.console.clear()
        self.start_btn.setText("Stop")

        infinite = self.infinite_checkbox.isChecked()
        count = None if infinite else self.count_input.value()

        self.thread = QThread()
        self.worker = PingWorker(ip=ip, count=count)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.output.connect(self.append_colored)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.on_finished)

        self.thread.start()

    def stop_ping(self):
        if self.worker:
            self.worker.stop()

    def append_colored(self, text: str):
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

    def on_finished(self):
        self.start_btn.setText("Ping")
        self.thread = None
        self.worker = None
