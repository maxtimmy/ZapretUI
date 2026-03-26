from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class StatusCard(QFrame):
    def __init__(self, title: str, value: str = '-'):
        super().__init__()
        self.setObjectName('card')
        x = QVBoxLayout(self)
        x.setContentsMargins(16, 14, 16, 14)
        x.setSpacing(6)

        self.t = QLabel(title)
        self.t.setObjectName('cardTitle')
        self.v = QLabel(value)
        self.v.setObjectName('cardValue')

        x.addWidget(self.t)
        x.addWidget(self.v)
        x.addStretch()

    def set_value(self, value: str):
        self.v.setText(str(value))
