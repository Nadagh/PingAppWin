# presentation/qt/presenters/ping_presenter.py

class PingPresenter:
    """
    Presenter для PingTab.

    Отвечает за:
    - реакцию на действия пользователя
    - подготовку данных для UI
    - координацию между UI и Application (позже)
    """


    def __init__(self, view, use_case) -> None:
        """
        view: PingTab
        """

        self.view = view
        self.use_case = use_case


    def on_start_clicked(self) -> None:
        self.use_case.start_ping()


    def _set_all_rows_pending(self) -> None:
        table = self.view.table_panel.table
        for row in range(table.rowCount()):
            item = table.item(row, 1)
            if item:
                item.setText("В процессе")
