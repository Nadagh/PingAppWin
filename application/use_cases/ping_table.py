class PingTableUseCase:
    """
    application-layer use case.
    Временно — без реального ping.
    """

    def __init__(self, view) -> None:
        self.view = view

    def start_ping(self) -> None:
        """
        TODO:
        Подключить domain + infrastructure.
        """
        table = self.view.table_panel.table
        for row in range(table.rowCount()):
            item = table.item(row, 1)
            if item:
                item.setText("В процессе")
