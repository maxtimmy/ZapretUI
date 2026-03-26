from app.core.utils import now_text


class LogService:
    def __init__(self):
        self._items = []

    def add(self, level: str, message: str):
        row = f'[{now_text()}] [{level.upper()}] {message}'
        self._items.append(row)
        return row

    def info(self, message: str):
        return self.add('info', message)

    def error(self, message: str):
        return self.add('error', message)

    def warning(self, message: str):
        return self.add('warning', message)

    def clear(self):
        self._items.clear()

    def all(self):
        return list(self._items)

    def tail(self, n=100):
        return self._items[-n:]
