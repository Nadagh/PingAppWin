import asyncio
import threading

from application import NetworkScanUseCase


class NetworkScanPresenter:
    """
    Presenter для NetworkScanTab.
    Поток и asyncio управляются здесь, по канону PingPresenter.
    """

    def __init__(self, view) -> None:
        self.view = view
        self._use_case: NetworkScanUseCase | None = None
        self._thread: threading.Thread | None = None

    # =========================
    # UI actions
    # =========================

    def on_start_clicked(self) -> None:
        # reset UI
        self.view.tables.clear()
        self.view.progress.reset()
        self._set_running(True)

        # create use case
        self._use_case = NetworkScanUseCase(
            ping_executor=None  # подменяется в тестах / wiring-е
        )

        # start background thread
        self._thread = threading.Thread(
            target=self._run_async_use_case,
            daemon=True,
        )
        self._thread.start()

    def on_stop_clicked(self) -> None:
        if self._use_case:
            self._use_case.cancel()
        self._set_running(False)

    # =========================
    # Async runner
    # =========================

    def _run_async_use_case(self) -> None:
        try:
            result = self._use_case.execute(
                    raw_ranges = self.view.input_panel.input_edit.text(),
                    count = self.view.controls.count_input.value(),
                    max_parallel = self.view.controls.max_parallel_input.value(),
                    on_progress = self._on_progress,
                    on_result = self._on_result,
                    )

            if asyncio.iscoroutine(result):
                asyncio.run(result)

        finally:
            self._set_running(False)


    # =========================
    # Callbacks from use case
    # =========================

    def _on_result(self, ip: str, alive: bool) -> None:
        table = self.view.tables.success if alive else self.view.tables.fail

        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, ip)


    def _on_progress(self, done: int, total: int) -> None:
        self.view.progress.bar.setMaximum(total)
        self.view.progress.bar.setValue(done)
        self.view.progress.label.setText(f"Прогресс: {done} / {total}")

    # =========================
    # Helpers
    # =========================

    def _set_running(self, running: bool) -> None:
        self.view.controls.start_btn.setEnabled(not running)
        self.view.controls.stop_btn.setEnabled(running)
