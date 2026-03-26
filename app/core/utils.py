from datetime import datetime


def now_text() -> str:
    return datetime.now().strftime('%H:%M:%S')


def clean_domains(items):
    out = []
    for x in items:
        s = str(x).strip()
        if s and s not in out:
            out.append(s)
    return out
