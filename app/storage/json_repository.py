import json
from pathlib import Path


class JsonRepository:
    def read(self, path: str | Path, default=None):
        p = Path(path)
        if not p.exists():
            return {} if default is None else default
        txt = p.read_text(encoding="utf-8").strip()
        if not txt:
            return {} if default is None else default
        try:
            return json.loads(txt)
        except json.JSONDecodeError as e:
            raise ValueError(f"invalid json in {p}: {e}") from e

    def write(self, path: str | Path, data) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
