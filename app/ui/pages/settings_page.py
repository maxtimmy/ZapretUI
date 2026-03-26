from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QCheckBox, QPushButton

from app.models.settings import Settings


class SettingsPage(QWidget):
    save_requested = Signal()

    def __init__(self):
        super().__init__()
        self.profile_box = QComboBox()
        self.theme_box = QComboBox()
        self.theme_box.addItems(["dark", "light"])
        self.tray_box = QCheckBox("minimize to tray")
        self.auto_box = QCheckBox("auto save")
        self.save_btn = QPushButton("save settings")
        self.save_btn.clicked.connect(self.save_requested.emit)

        form = QFormLayout(self)
        form.addRow("default profile", self.profile_box)
        form.addRow("theme", self.theme_box)
        form.addRow("", self.tray_box)
        form.addRow("", self.auto_box)
        form.addRow(self.save_btn)

    def set_data(self, s: Settings, profile_names: list[str]):
        self.profile_box.clear()
        self.profile_box.addItems(profile_names)
        self.profile_box.setCurrentText(s.default_profile)
        self.theme_box.setCurrentText(s.theme)
        self.tray_box.setChecked(s.to_tray)
        self.auto_box.setChecked(s.auto_save)

    def read_data(self) -> Settings:
        return Settings(
            default_profile=self.profile_box.currentText(),
            theme=self.theme_box.currentText(),
            to_tray=self.tray_box.isChecked(),
            auto_save=self.auto_box.isChecked(),
            window_width=1280,
            window_height=820,
        )
