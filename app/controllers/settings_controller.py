from app.models.settings import Settings


class SettingsController:
    def build(self, data: dict):
        return Settings.from_dict(data)
