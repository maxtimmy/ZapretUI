from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.ui.widgets.log_viewer import LogViewer
from app.ui.widgets.status_card import StatusCard


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        v.setSpacing(12)

        row = QHBoxLayout()
        self.status_card = StatusCard('статус')
        self.profile_card = StatusCard('профиль')
        self.interface_card = StatusCard('интерфейс')
        self.dns_card = StatusCard('dns')

        row.addWidget(self.status_card)
        row.addWidget(self.profile_card)
        row.addWidget(self.interface_card)
        row.addWidget(self.dns_card)

        box = QGroupBox('быстрые действия')
        x = QHBoxLayout(box)
        self.start_btn = QPushButton('старт')
        self.stop_btn = QPushButton('стоп')
        self.restart_btn = QPushButton('рестарт')
        x.addWidget(self.start_btn)
        x.addWidget(self.stop_btn)
        x.addWidget(self.restart_btn)
        x.addStretch()

        self.events = LogViewer()
        self.events.setMinimumHeight(220)

        v.addLayout(row)
        v.addWidget(box)
        v.addWidget(QLabel('последние события'))
        v.addWidget(self.events)

    def set_status(self, x):
        self.status_card.set_value(x)

    def set_profile(self, x):
        self.profile_card.set_value(x)

    def set_interface(self, x):
        self.interface_card.set_value(x)

    def set_dns(self, x):
        self.dns_card.set_value(x)

    def add_event(self, x):
        self.events.add_line(x)
