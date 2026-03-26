from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit, QLabel


class ProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("new profile")
        self.edit = QLineEdit()
        box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)

        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("profile name"))
        lay.addWidget(self.edit)
        lay.addWidget(box)

    def value(self) -> str:
        return self.edit.text().strip()
