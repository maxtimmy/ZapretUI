from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('о программе')
        v = QVBoxLayout(self)
        v.addWidget(QLabel('net control\nбезопасный каркас десктоп-приложения'))
