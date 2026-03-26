import subprocess
import time
from typing import Callable

from PySide6.QtCore import QThread, Signal

from app.core.constants import STATUS_ERROR, STATUS_RUNNING, STATUS_STARTING, STATUS_STOPPED
from app.models.profile import Profile


class ProcessWorker(QThread):
    line = Signal(str)
    status = Signal(str)
    pid_changed = Signal(int)

    def __init__(self, profile: Profile):
        super().__init__()
        self.profile = profile
        self._active = True
        self._proc = None

    def run(self):
        cmd = self.profile.command.strip()
        if not cmd:
            self.line.emit('команда не указана')
            self.status.emit(STATUS_ERROR)
            return

        self.status.emit(STATUS_STARTING)
        self.line.emit(f'запуск: {cmd}')

        try:
            self._proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            self.pid_changed.emit(self._proc.pid or 0)
            self.status.emit(STATUS_RUNNING)

            while self._active:
                if self._proc.poll() is not None:
                    break

                line = self._proc.stdout.readline()
                if line:
                    self.line.emit(line.rstrip())
                else:
                    time.sleep(0.1)

            if not self._active and self._proc and self._proc.poll() is None:
                self.line.emit('остановка процесса')
                self._proc.terminate()
                try:
                    self._proc.wait(timeout=3)
                except Exception:
                    self._proc.kill()

            code = self._proc.poll()
            self.line.emit(f'процесс завершен, код: {code}')
            self.status.emit(STATUS_STOPPED)
        except Exception as e:
            self.line.emit(f'ошибка запуска: {e}')
            self.status.emit(STATUS_ERROR)

    def stop(self):
        self._active = False


class ProcessService:
    def __init__(self):
        self.worker: ProcessWorker | None = None

    def start(self, profile: Profile, on_line: Callable, on_status: Callable, on_pid: Callable):
        if self.is_running():
            return False
        self.worker = ProcessWorker(profile)
        self.worker.line.connect(on_line)
        self.worker.status.connect(on_status)
        self.worker.pid_changed.connect(on_pid)
        self.worker.start()
        return True

    def stop(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()

    def restart(self, profile: Profile, on_line: Callable, on_status: Callable, on_pid: Callable):
        self.stop()
        return self.start(profile, on_line, on_status, on_pid)

    def is_running(self):
        return bool(self.worker and self.worker.isRunning())
