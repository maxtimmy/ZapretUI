from PySide6.QtWidgets import QDialog, QVBoxLayout

from app.ui.widgets.profile_form import ProfileForm


class ProfileDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('профиль')
        v = QVBoxLayout(self)
        self.form = ProfileForm()
        v.addWidget(self.form)
