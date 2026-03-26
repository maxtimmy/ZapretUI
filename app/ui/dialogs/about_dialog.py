from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("about")
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Net Control\nPySide6 desktop app"))
