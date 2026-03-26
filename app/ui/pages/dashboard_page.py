from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit, QLabel

from app.models.profile import Profile
from app.ui.widgets.status_card import StatusCard
from app.ui.widgets.hint_button import HintButton


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setSpacing(12)

        cards = QHBoxLayout()

        self.status_card = StatusCard("status")
        self.profile_card = StatusCard("profile")
        self.interface_card = StatusCard("interface")
        self.dns_card = StatusCard("dns")

        cards.addWidget(self.status_card)
        cards.addWidget(self.profile_card)
        cards.addWidget(self.interface_card)
        cards.addWidget(self.dns_card)

        box = QGroupBox("quick actions")
        row = QHBoxLayout(box)

        self.start_btn = HintButton("start")
        self.stop_btn = HintButton("stop")
        self.restart_btn = HintButton("restart")

        row.addWidget(self.start_btn)
        row.addWidget(self.stop_btn)
        row.addWidget(self.restart_btn)
        row.addStretch()

        self.events = QTextEdit()
        self.events.setReadOnly(True)
        self.events.setMinimumHeight(220)

        root.addLayout(cards)
        root.addWidget(box)
        root.addWidget(QLabel("recent events"))
        root.addWidget(self.events)

    def set_status(self, status: str):
        self.status_card.set_status_value(status)

    def set_profile_info(self, p: Profile):
        self.profile_card.set_value(p.name or "-")
        self.interface_card.set_value(p.interface or "-")
        self.dns_card.set_value(p.dns or "-")

    def append_event(self, text: str):
        self.events.append(text)

    def set_recent_logs(self, items: list[str]):
        self.events.clear()
        for x in items[-200:]:
            self.events.append(x)