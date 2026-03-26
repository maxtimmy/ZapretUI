from PySide6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QPushButton, QWidget


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        f = QFormLayout(self)

        self.default_profile = QComboBox()
        self.theme = QComboBox()
        self.theme.addItems(['dark', 'light'])
        self.to_tray = QCheckBox('сворачивать в трей')
        self.auto_save = QCheckBox('автосохранять конфиг')
        self.save_btn = QPushButton('сохранить настройки')

        f.addRow('профиль по умолчанию', self.default_profile)
        f.addRow('тема', self.theme)
        f.addRow('', self.to_tray)
        f.addRow('', self.auto_save)
        f.addRow(self.save_btn)

    def set_data(self, data: dict, profile_names: list[str]):
        self.default_profile.clear()
        self.default_profile.addItems(profile_names)
        self.default_profile.setCurrentText(data.get('default_profile', 'default'))
        self.theme.setCurrentText(data.get('theme', 'dark'))
        self.to_tray.setChecked(bool(data.get('to_tray', True)))
        self.auto_save.setChecked(bool(data.get('auto_save', True)))

    def get_data(self):
        return {
            'default_profile': self.default_profile.currentText(),
            'theme': self.theme.currentText(),
            'to_tray': self.to_tray.isChecked(),
            'auto_save': self.auto_save.isChecked(),
        }
