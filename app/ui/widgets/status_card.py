from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class StatusCard(QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setObjectName("statusCard")

        box = QVBoxLayout(self)
        box.setContentsMargins(16, 14, 16, 14)
        box.setSpacing(6)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("statusCardTitle")

        self.value_label = QLabel("-")
        self.value_label.setObjectName("statusCardValue")

        box.addWidget(self.title_label)
        box.addWidget(self.value_label)
        box.addStretch()

    def set_value(self, value: str):
        self.value_label.setText(str(value))

    def set_status_value(self, value: str):
        s = (value or "").strip().lower()
        self.value_label.setText(value)

        self.value_label.setProperty("statusState", s)
        self.value_label.style().unpolish(self.value_label)
        self.value_label.style().polish(self.value_label)
        self.value_label.update()