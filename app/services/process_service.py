import subprocess
import threading
import time
from typing import Callable

from app.core.constants import STATUS_ERROR, STATUS_RUNNING, STATUS_STARTING, STATUS_STOPPED
from app.models.profile import Profile


class ProcessService:
    def __init__(self):
        self.proc: subprocess.Popen | None = None
        self.status = STATUS_STOPPED
        self._reader: threading.Thread | None = None
        self._stop_flag = False
        self._on_log: Callable[[str], None] | None = None
        self._on_status: Callable[[str], None] | None = None

    def set_callbacks(self, on_log=None, on_status=None):
        self._on_log = on_log
        self._on_status = on_status

    def _emit_log(self, s: str):
        if self._on_log:
            self._on_log(s)

    def _emit_status(self, s: str):
        self.status = s
        if self._on_status:
            self._on_status(s)

    def is_running(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def get_status(self) -> str:
        return self.status

    def start(self, profile: Profile) -> None:
        if self.is_running():
            raise RuntimeError("process already running")
        ok, msg = profile.validate(require_command=True)
        if not ok:
            raise ValueError(msg)

        self._stop_flag = False
        self._emit_status(STATUS_STARTING)
        self._emit_log(f"starting: {profile.command}")
        try:
            self.proc = subprocess.Popen(
                profile.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        except Exception as e:
            self.proc = None
            self._emit_status(STATUS_ERROR)
            self._emit_log(f"start error: {e}")
            raise

        self._emit_status(STATUS_RUNNING)
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()

    def _read_loop(self):
        if not self.proc or not self.proc.stdout:
            return
        while not self._stop_flag and self.proc and self.proc.poll() is None:
            line = self.proc.stdout.readline()
            if line:
                self._emit_log(line.rstrip())
            else:
                time.sleep(0.05)

        if self.proc:
            rc = self.proc.poll()
            self._emit_log(f"process exited with code: {rc}")
        self._emit_status(STATUS_STOPPED)

    def stop(self) -> None:
        if not self.is_running():
            self._emit_status(STATUS_STOPPED)
            return
        self._stop_flag = True
        assert self.proc is not None
        self._emit_log("stopping process")
        self.proc.terminate()
        try:
            self.proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(timeout=3)
        self._emit_status(STATUS_STOPPED)

    def restart(self, profile: Profile) -> None:
        self.stop()
        self.start(profile)
