from app.core.config import LOG_FILE
from app.core.utils import now_str
from app.storage.file_manager import FileManager


class LogService:
    def __init__(self, fm: FileManager | None = None):
        self.fm = fm or FileManager()
        self._items: list[str] = []

    def _push(self, level: str, msg: str) -> str:
        line = f"[{now_str()}] [{level}] {msg}"
        self._items.append(line)
        try:
            old = ""
            if self.fm.exists(LOG_FILE):
                old = self.fm.read_text(LOG_FILE)
            self.fm.save_text(LOG_FILE, old + ("\n" if old else "") + line)
        except Exception:
            pass
        return line

    def info(self, msg: str) -> str:
        return self._push("INFO", msg)

    def warning(self, msg: str) -> str:
        return self._push("WARN", msg)

    def error(self, msg: str) -> str:
        return self._push("ERROR", msg)

    def get_all(self) -> list[str]:
        return self._items[:]

    def clear(self) -> None:
        self._items.clear()

    def dump_text(self) -> str:
        return "\n".join(self._items)

    def save_to_file(self, path: str) -> None:
        self.fm.save_text(path, self.dump_text())
