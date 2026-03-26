from pathlib import Path


class FileManager:
    def write_text(self, path: Path, text: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def exists(self, path: Path) -> bool:
        return path.exists()
