# presentation/qt/presenters/ping_presenter.py
from PySide6.QtGui import QColor


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
        results = self.use_case.prepare_ping(ip_values)
        self._apply_results(results)


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


    def _apply_results(self, results: list[tuple[str, object]]) -> None:
        table = self.view.table_panel.table

        for row, (_, status) in enumerate(results):
            status_item = table.item(row, 1)
            if not status_item:
                continue

            if status.name == "SUCCESS":
                status_item.setText("Успешно")
                status_item.setBackground(QColor("#d1e7dd"))  # мягкий зелёный

            elif status.name == "FAILURE":
                status_item.setText("Нет ответа")
                status_item.setBackground(QColor("#f8d7da"))  # мягкий красный

            elif status.name == "ERROR":
                status_item.setText("Ошибка IP")
                status_item.setBackground(QColor("#f8d7da"))

            elif status.name == "MISSING":
                status_item.setText("Не указан IP")
                status_item.setBackground(QColor("#e2e3e5"))

