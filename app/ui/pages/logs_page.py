from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from app.ui.widgets.log_viewer import LogViewer


class LogsPage(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        self.viewer = LogViewer()
        v.addWidget(self.viewer)

        x = QHBoxLayout()
        self.clear_btn = QPushButton('очистить')
        self.save_btn = QPushButton('сохранить лог')
        x.addWidget(self.clear_btn)
        x.addWidget(self.save_btn)
        x.addStretch()
        v.addLayout(x)
