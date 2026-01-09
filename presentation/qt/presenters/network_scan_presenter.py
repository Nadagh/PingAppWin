# presentation/qt/presenters/network_scan_presenter.py

class NetworkScanPresenter:
    """
    Presenter для NetworkScanTab.

    На данном этапе:
    - управляет состоянием UI
    - НЕ выполняет сканирование
    - НЕ парсит диапазоны
    """

    def __init__(self, view) -> None:
        self.view = view

    def on_start_clicked(self) -> None:
        # UI-only поведение
        self.view.tables.clear()
        self.view.progress.reset()

        self._set_running(True)

    def on_stop_clicked(self) -> None:
        self._set_running(False)

    def _set_running(self, running: bool) -> None:
        self.view.controls.start_btn.setEnabled(not running)
        self.view.controls.stop_btn.setEnabled(running)
