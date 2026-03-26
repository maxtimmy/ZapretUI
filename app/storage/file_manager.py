from pathlib import Path


class FileManager:
    def ensure_dir(self, path: str | Path) -> Path:
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def exists(self, path: str | Path) -> bool:
        return Path(path).exists()

    def save_text(self, path: str | Path, text: str) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def read_text(self, path: str | Path) -> str:
        return Path(path).read_text(encoding="utf-8")
