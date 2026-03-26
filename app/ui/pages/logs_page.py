from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from app.ui.widgets.log_viewer import LogViewer


class LogsPage(QWidget):
    save_requested = Signal()
    clear_requested = Signal()

    def __init__(self):
        super().__init__()
        self.viewer = LogViewer()
        self.clear_btn = QPushButton("clear")
        self.save_btn = QPushButton("save log")
        self.clear_btn.clicked.connect(self.clear_requested.emit)
        self.save_btn.clicked.connect(self.save_requested.emit)

        row = QHBoxLayout()
        row.addWidget(self.clear_btn)
        row.addWidget(self.save_btn)
        row.addStretch()

        root = QVBoxLayout(self)
        root.addWidget(self.viewer)
        root.addLayout(row)

    def append_log(self, text: str):
        self.viewer.append_line(text)

    def set_logs(self, items: list[str]):
        self.viewer.set_lines(items)

    def clear_logs(self):
        self.viewer.clear_logs()
