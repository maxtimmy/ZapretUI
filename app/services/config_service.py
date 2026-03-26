from copy import deepcopy

from app.core.config import CONFIG_PATH
from app.core.constants import DEFAULT_PROFILE, DEFAULT_SETTINGS
from app.models.profile import Profile
from app.models.settings import Settings
from app.storage.json_repository import JsonRepository


class ConfigService:
    def __init__(self, repo: JsonRepository):
        self.repo = repo

    def load(self):
        data = self.repo.read(CONFIG_PATH)
        if not data:
            return self.default_payload()

        profiles = [Profile.from_dict(x) for x in data.get('profiles', [])]
        if not profiles:
            profiles = [Profile.from_dict(deepcopy(DEFAULT_PROFILE))]

        settings = Settings.from_dict(data.get('settings', deepcopy(DEFAULT_SETTINGS)))
        return {'profiles': profiles, 'settings': settings}

    def save(self, profiles: list[Profile], settings: Settings):
        payload = {
            'profiles': [x.to_dict() for x in profiles],
            'settings': settings.to_dict(),
        }
        self.repo.write(CONFIG_PATH, payload)

    def export_to(self, path, profiles: list[Profile], settings: Settings):
        payload = {
            'profiles': [x.to_dict() for x in profiles],
            'settings': settings.to_dict(),
        }
        self.repo.write(path, payload)

    def import_from(self, path):
        data = self.repo.read(path)
        profiles = [Profile.from_dict(x) for x in data.get('profiles', [])]
        settings = Settings.from_dict(data.get('settings', {}))
        return {'profiles': profiles, 'settings': settings}

    def default_payload(self):
        return {
            'profiles': [Profile.from_dict(deepcopy(DEFAULT_PROFILE))],
            'settings': Settings.from_dict(deepcopy(DEFAULT_SETTINGS)),
        }
