from PySide6.QtWidgets import QTextEdit


class LogViewer(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def append_line(self, text: str):
        self.append(text)

    def set_lines(self, items: list[str]):
        self.setPlainText("\n".join(items))

    def clear_logs(self):
        self.clear()
