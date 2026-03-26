from PySide6.QtWidgets import QTextEdit


class LogViewer(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def add_line(self, line: str):
        self.append(line)
