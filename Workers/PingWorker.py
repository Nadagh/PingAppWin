import subprocess
from PySide6.QtCore import QObject, Signal, Slot


class PingWorker(QObject):
    output = Signal(str)
    finished = Signal()

    def __init__(self, ip: str, count: int | None):
        super().__init__()
        self.ip = ip
        self.count = count
        self.process: subprocess.Popen | None = None
        self._running = True

    @Slot()
    def run(self):
        cmd = ["ping", self.ip]

        if self.count is not None:
            cmd += ["-n", str(self.count)]
        else:
            cmd += ["-t"]

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="cp866"
        )

        for line in self.process.stdout:
            if not self._running:
                break
            self.output.emit(line.rstrip())

        self.stop()
        self.finished.emit()

    def stop(self):
        self._running = False
        if self.process and self.process.poll() is None:
            self.process.terminate()
