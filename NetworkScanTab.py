import asyncio
import ipaddress
import subprocess
import re
from itertools import product

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QSpinBox, QHeaderView, QProgressBar
)

from AsyncPingWorker import AsyncPingWorker  # Асинхронный воркер пинга

class NetworkScanTab(QWidget):
    def __init__(self):
        super().__init__()

        # ---------- INPUT ----------
        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText(
            "Примеры:\n"
            "150.102.95.5-100\n"
            "150.102.1-255.25-50\n"
            "150.102.0.0/16\n"
            "150.102.0.0 - 150.102.255.255"
        )

        self.count_input = QSpinBox()
        self.count_input.setRange(1, 10)
        self.count_input.setValue(1)

        self.max_parallel_input = QSpinBox()
        self.max_parallel_input.setRange(1, 300)
        self.max_parallel_input.setValue(100)  # default max parallel

        self.start_btn = QPushButton("Сканировать")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)

        self.adapters_btn = QPushButton("Адаптеры")

        # ---------- TABLES ----------
        self.success_table = QTableWidget(0, 1)
        self.success_table.setHorizontalHeaderLabels(["Успешно"])
        self.success_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.fail_table = QTableWidget(0, 1)
        self.fail_table.setHorizontalHeaderLabels(["Нет ответа"])
        self.fail_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # ---------- PROGRESS ----------
        self.progress_label = QLabel("Прогресс: 0 / 0")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)

        # ---------- LAYOUT ----------
        top = QHBoxLayout()
        top.addWidget(QLabel("Пакетов:"))
        top.addWidget(self.count_input)
        top.addWidget(QLabel("Макс параллельных:"))
        top.addWidget(self.max_parallel_input)
        top.addSpacing(20)
        top.addWidget(self.adapters_btn)
        top.addStretch()
        top.addWidget(self.start_btn)
        top.addWidget(self.stop_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self.input_edit)
        layout.addLayout(top)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        tables_layout = QHBoxLayout()
        tables_layout.addWidget(self.success_table)
        tables_layout.addWidget(self.fail_table)
        layout.addLayout(tables_layout)

        # ---------- STATE ----------
        self.queue = asyncio.Queue()
        self.semaphore = None
        self.status_items = {}  # ip -> (table, QTableWidgetItem)
        self.loop = asyncio.new_event_loop()
        self.total_addresses = 0
        self.processed_addresses = 0
        self.running_tasks = []

        # ---------- SIGNALS ----------
        self.start_btn.clicked.connect(self.start_scan)
        self.stop_btn.clicked.connect(self.stop_scan)
        self.adapters_btn.clicked.connect(self.scan_adapters)

        # ---------- TIMER ----------
        self.timer = QTimer()
        self.timer.timeout.connect(self._step_async)
        self.timer.start(10)

    # ======================================================
    # ASYNC LOOP BRIDGE
    # ======================================================
    def _step_async(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    # ======================================================
    # ENTRY
    # ======================================================
    def start_scan(self):
        self._reset()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        max_parallel = self.max_parallel_input.value()
        self.semaphore = asyncio.Semaphore(max_parallel)

        all_ips = list(self._iter_input(self.input_edit.toPlainText()))
        self.total_addresses = len(all_ips)
        self.processed_addresses = 0
        self.progress_bar.setMaximum(self.total_addresses)
        self.progress_bar.setValue(0)
        self.progress_label.setText(f"Прогресс: 0 / {self.total_addresses}")

        for ip in all_ips:
            self._add_initial(ip)
            self.queue.put_nowait(ip)

        self.loop.create_task(self._runner())

    def scan_adapters(self):
        self._reset()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        max_parallel = self.max_parallel_input.value()
        self.semaphore = asyncio.Semaphore(max_parallel)

        for net in self._get_networks_from_adapters():
            for ip in net.hosts():
                ip = str(ip)
                self._add_initial(ip)
                self.queue.put_nowait(ip)

        self.total_addresses = self.queue.qsize()
        self.processed_addresses = 0
        self.progress_bar.setMaximum(self.total_addresses)
        self.progress_bar.setValue(0)
        self.progress_label.setText(f"Прогресс: 0 / {self.total_addresses}")

        self.loop.create_task(self._runner())

    # ======================================================
    # STOP
    # ======================================================
    def stop_scan(self):
        while not self.queue.empty():
            self.queue.get_nowait()
            self.queue.task_done()

        for task in self.running_tasks:
            task.cancel()
        self.running_tasks.clear()

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    # ======================================================
    # ASYNC CORE
    # ======================================================
    async def _runner(self):
        while not self.queue.empty():
            ip = await self.queue.get()
            await self.semaphore.acquire()

            self._set_in_process(ip)

            worker = AsyncPingWorker(ip, self.count_input.value())
            task = self.loop.create_task(worker.run())
            self.running_tasks.append(task)

            def _callback(fut, ip=ip):
                try:
                    success = fut.result()
                except asyncio.CancelledError:
                    success = False
                self._on_finished(ip, success)
                self.semaphore.release()
                if fut in self.running_tasks:
                    self.running_tasks.remove(fut)

            task.add_done_callback(_callback)

    # ======================================================
    # CALLBACKS
    # ======================================================
    def _on_finished(self, ip, success):
        old_table, old_item = self.status_items[ip]
        row_index = old_table.indexFromItem(old_item).row()
        old_table.removeRow(row_index)

        table = self.success_table if success else self.fail_table
        row = table.rowCount()
        table.insertRow(row)
        new_item = QTableWidgetItem(ip)
        new_item.setBackground(QColor("#00aa00") if success else QColor("#cc0000"))
        new_item.setData(Qt.UserRole, ip)
        table.setItem(table.rowCount() - 1, 0, new_item)
        self.status_items[ip] = (table, new_item)

        self._sort_table(table)

        self.processed_addresses += 1
        self.progress_bar.setValue(self.processed_addresses)
        self.progress_label.setText(f"Прогресс: {self.processed_addresses} / {self.total_addresses}")

        if self.processed_addresses >= self.total_addresses:
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

    # ======================================================
    # TABLE MANAGEMENT
    # ======================================================
    def _add_initial(self, ip):
        row = self.fail_table.rowCount()
        self.fail_table.insertRow(row)
        item = QTableWidgetItem(f"{ip} — Ожидание")
        item.setBackground(QColor("#555555"))
        item.setData(Qt.UserRole, ip)
        self.fail_table.setItem(row, 0, item)
        self.status_items[ip] = (self.fail_table, item)

    def _set_in_process(self, ip):
        table, item = self.status_items[ip]
        item.setText(f"{ip} — В процессе")
        item.setBackground(QColor("#ffaa00"))
        item.setData(Qt.UserRole, ip)
        self._sort_table(table)

    def _sort_table(self, table):
        items = []
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item:
                items.append(item)
        items.sort(key=lambda x: int(ipaddress.IPv4Address(x.data(Qt.UserRole))))
        for i, item in enumerate(items):
            table.setItem(i, 0, item)

    def _reset(self):
        self.success_table.setRowCount(0)
        self.fail_table.setRowCount(0)
        self.status_items.clear()
        self.queue = asyncio.Queue()
        self.running_tasks.clear()
        self.progress_bar.setValue(0)
        self.progress_label.setText("Прогресс: 0 / 0")
        self.total_addresses = 0
        self.processed_addresses = 0

    # ======================================================
    # INPUT PARSING
    # ======================================================
    def _iter_input(self, text):
        for line in text.splitlines():
            line = line.strip().replace(" ", "")
            if not line:
                continue

            if "/" in line:
                for ip in ipaddress.ip_network(line, strict=False).hosts():
                    yield str(ip)

            elif "-" in line and all("." in p for p in line.split("-")):
                a, b = line.split("-")
                start = int(ipaddress.IPv4Address(a))
                end = int(ipaddress.IPv4Address(b))
                for i in range(start, end + 1):
                    yield str(ipaddress.IPv4Address(i))

            else:
                parts = line.split(".")
                ranges = []
                for p in parts:
                    if "-" in p:
                        x, y = map(int, p.split("-"))
                        ranges.append(range(x, y + 1))
                    else:
                        ranges.append([int(p)])
                for combo in product(*ranges):
                    yield ".".join(map(str, combo))

    # ======================================================
    # ADAPTERS
    # ======================================================
    def _get_networks_from_adapters(self):
        try:
            output = subprocess.check_output(
                "ipconfig", text=True, encoding="cp866", errors="ignore"
            )
        except Exception:
            return []

        ip_re = re.compile(r"IPv4[^:]*:\s*([\d\.]+)")
        mask_re = re.compile(r"(Subnet Mask|Маска подсети)[^:]*:\s*([\d\.]+)")

        ips = ip_re.findall(output)
        masks = [m[1] for m in mask_re.findall(output)]

        nets = []
        for ip, mask in zip(ips, masks):
            try:
                nets.append(ipaddress.IPv4Network(f"{ip}/{mask}", strict=False))
            except Exception:
                pass
        return nets
