import ipaddress

from PySide6.QtCore import QThread
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QSpinBox, QHeaderView
)

from Workers.PingWorker import PingWorker


class PingTab(QWidget):
    def __init__(self):
        super().__init__()

        # --- Global settings ---
        count_label = QLabel("Количество запросов:")
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 10000)
        self.count_input.setValue(4)

        # --- Buttons ---
        self.add_btn = QPushButton("Добавить")
        self.remove_btn = QPushButton("Удалить")
        self.start_btn = QPushButton("Ping")

        # --- Table ---
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["IP адрес", "Статус"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # фиксированная ширина IP
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 180)

        # статус растягивается
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        # --- Layout ---
        controls = QHBoxLayout()
        controls.addWidget(count_label)
        controls.addWidget(self.count_input)
        controls.addSpacing(20)
        controls.addWidget(self.add_btn)
        controls.addWidget(self.remove_btn)
        controls.addStretch()
        controls.addWidget(self.start_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(controls)
        layout.addWidget(self.table)

        # --- State ---
        self.threads: dict[int, QThread] = {}
        self.workers: dict[int, PingWorker] = {}
        self.has_success: dict[int, bool] = {}
        self.has_failure: dict[int, bool] = {}
        self.active_pings: int = 0

        # --- Signals ---
        self.add_btn.clicked.connect(self.add_row)
        self.remove_btn.clicked.connect(self.remove_selected_rows)
        self.start_btn.clicked.connect(self.start_ping)

        # минимум одна строка
        self.add_row()

    # -------------------------
    # Table management
    # -------------------------

    def add_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        ip_item = QTableWidgetItem("")
        status_item = QTableWidgetItem("Ожидание")
        status_item.setBackground(QColor("#cccccc"))

        self.table.setItem(row, 0, ip_item)
        self.table.setItem(row, 1, status_item)

    def remove_selected_rows(self):
        if self.table.rowCount() <= 1:
            return

        rows = sorted(
            {index.row() for index in self.table.selectedIndexes()},
            reverse=True
        )

        for row in rows:
            if self.table.rowCount() > 1:
                self.table.removeRow(row)

    # -------------------------
    # Ping logic
    # -------------------------

    def start_ping(self):
        self._clear_state()
        self.start_btn.setEnabled(False)

        count = self.count_input.value()
        self.active_pings = 0

        for row in range(self.table.rowCount()):
            ip_item = self.table.item(row, 0)
            if not ip_item:
                continue

            ip = ip_item.text().strip()
            if not ip:
                self._set_status(row, "Нет IP", "#cc0000")
                continue

            if not self._is_valid_ip(ip):
                self._set_status(row, "Некорректный IP", "#cc0000")
                continue

            self.has_success[row] = False
            self.has_failure[row] = False
            self._set_status(row, "В процессе", "#ffcc00")
            self._start_worker(row, ip, count)
            self.active_pings += 1

        if self.active_pings == 0:
            self.start_btn.setEnabled(True)

    def _start_worker(self, row: int, ip: str, count: int):
        thread = QThread()
        worker = PingWorker(ip=ip, count=count)
        worker.moveToThread(thread)

        worker.output.connect(lambda text, r=row: self._on_output(r, text))
        worker.finished.connect(lambda r=row: self._on_finished(r))

        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        self.threads[row] = thread
        self.workers[row] = worker

        thread.started.connect(worker.run)
        thread.start()

    def _on_output(self, row: int, text: str):
        text_l = text.lower()
        # общий сбой (рус. и англ.)
        if "сбой передачи" in text_l or "general failure" in text_l:
            self.has_failure[row] = True
        # успешный ответ
        if "ttl=" in text_l:
            self.has_success[row] = True

    def _on_finished(self, row: int):
        if self.has_failure.get(row):
            self._set_status(row, "Общий сбой", "#cc0000")
        elif self.has_success.get(row):
            self._set_status(row, "Успешно", "#00aa00")
        else:
            self._set_status(row, "Нет ответа", "#cc0000")

        self.active_pings -= 1
        if self.active_pings == 0:
            self.start_btn.setEnabled(True)

    # -------------------------
    # Helpers
    # -------------------------

    def _is_valid_ip(self, ip: str) -> bool:
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def _set_status(self, row: int, text: str, color: str):
        item = self.table.item(row, 1)
        if item:
            item.setText(text)
            item.setBackground(QColor(color))

    def _clear_state(self):
        self.threads.clear()
        self.workers.clear()
        self.has_success.clear()
        self.has_failure.clear()
