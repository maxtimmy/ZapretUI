from datetime import datetime


def now_str() -> str:
    return datetime.now().strftime("%H:%M:%S")


def is_blank(s: str | None) -> bool:
    return not s or not str(s).strip()


def safe_str(x) -> str:
    if x is None:
        return ""
    return str(x)


def normalize_domains(items) -> list[str]:
    out = []
    seen = set()
    for x in items or []:
        s = safe_str(x).strip()
        if not s:
            continue
        s = s.replace("http://", "").replace("https://", "").strip("/")
        if s and s not in seen:
            out.append(s)
            seen.add(s)
    return out
