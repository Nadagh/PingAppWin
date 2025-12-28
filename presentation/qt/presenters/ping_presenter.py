# presentation/qt/presenters/ping_presenter.py
import asyncio
import threading

from application.use_cases import AsyncPingTableUseCase
from domain import PingStatus
from presentation.qt.mappers import map_ping_status


class PingPresenter:
    """
    Presenter для PingTab.

    Отвечает за:
    - реакцию на действия пользователя
    - подготовку данных для UI
    - координацию между UI и application (позже)
    """


    def __init__(self, view, use_case) -> None:
        """
        view: PingTab
        """

        self.view = view
        self.use_case = use_case


    def on_start_clicked(self) -> None:
        ip_values = self._collect_ip_values()

        async_use_case = AsyncPingTableUseCase(
                on_result = self._on_async_result,
                max_concurrent = 50,
                )

        thread = threading.Thread(
                target = self._run_async_use_case,
                args = (async_use_case, ip_values),
                daemon = True,
                )
        thread.start()


    def _set_all_rows_pending(self) -> None:
        table = self.view.table_panel.table
        for row in range(table.rowCount()):
            item = table.item(row, 1)
            if item:
                item.setText("В процессе")


    def _collect_ip_values(self) -> list[str]:
        table = self.view.table_panel.table
        values: list[str] = []

        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item:
                values.append(item.text().strip())

        return values


    def _apply_results(self, results: list[tuple[str, PingStatus]]) -> None:
        table = self.view.table_panel.table

        for row, (_, status) in enumerate(results):
            status_item = table.item(row, 1)
            if not status_item:
                continue

            view_model = map_ping_status(status)
            status_item.setText(view_model.text)
            status_item.setBackground(view_model.color)


    def _on_async_result(self, row: int, status: PingStatus) -> None:
        table = self.view.table_panel.table
        item = table.item(row, 1)
        if not item:
            return

        vm = map_ping_status(status)
        item.setText(vm.text)
        item.setBackground(vm.color)


    def _run_async_use_case(self, use_case, ip_values: list[str]) -> None:
        asyncio.run(use_case.run(ip_values))

