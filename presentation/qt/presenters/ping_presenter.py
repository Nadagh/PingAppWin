import asyncio
import threading

from application.use_cases import AsyncPingTableUseCase
from domain import PingResultStatus
from presentation.qt.mappers import map_ping_result_status
from presentation.qt.mappers.ping_status_mapper import COLOR_IDLE
from presentation.qt.strings import STATUS_IDLE


class PingPresenter:
    """
    Presenter для PingTab.

    Отвечает за:
    - реакцию на действия пользователя
    - координацию между UI и application
    - обновление таблицы статусов
    """

    def __init__(self, view, use_case=None) -> None:
        self.view = view
        self._use_case = use_case
        self._worker_thread: threading.Thread | None = None

    # =========================
    # UI actions
    # =========================

    def on_start_clicked(self) -> None:
        ip_values = self._collect_ip_values()

        self._reset_statuses()
        self._set_running(True)

        self._use_case = AsyncPingTableUseCase(
            on_result=self._on_async_result,
            max_concurrent=self.view.controls.parallel_input.value(),
            timeout_ms=self.view.controls.timeout_input.value(),
        )

        self._worker_thread = threading.Thread(
            target=self._run_async_use_case,
            args=(self._use_case, ip_values),
            daemon=True,
        )
        self._worker_thread.start()

    def on_stop_clicked(self) -> None:
        if self._use_case:
            self._use_case.cancel()
        self._set_running(False)

    # =========================
    # Internal helpers
    # =========================

    def _collect_ip_values(self) -> list[str]:
        table = self.view.table_panel.table
        values: list[str] = []

        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item:
                values.append(item.text().strip())

        return values

    def _run_async_use_case(self, use_case: AsyncPingTableUseCase, ip_values: list[str]) -> None:
        asyncio.run(use_case.run(ip_values))
        self._set_running(False)

    def _on_async_result(self, row: int, status: PingResultStatus) -> None:
        table = self.view.table_panel.table
        item = table.item(row, 1)
        if not item:
            return

        vm = map_ping_result_status(status)
        item.setText(vm.text)
        item.setBackground(vm.color)

    def _reset_statuses(self) -> None:
        table = self.view.table_panel.table
        for row in range(table.rowCount()):
            item = table.item(row, 1)
            if item:
                item.setText(STATUS_IDLE)
                item.setBackground(COLOR_IDLE)

    def _set_running(self, running: bool) -> None:
        self.view.controls.start_btn.setEnabled(not running)
        self.view.controls.stop_btn.setEnabled(running)
