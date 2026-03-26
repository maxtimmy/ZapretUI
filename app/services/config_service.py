from pathlib import Path

from app.core.config import CONFIG_FILE
from app.models.profile import Profile
from app.models.settings import Settings
from app.storage.json_repository import JsonRepository


class ConfigService:
    def __init__(self, repo: JsonRepository | None = None, path: Path | None = None):
        self.repo = repo or JsonRepository()
        self.path = path or CONFIG_FILE

    def default_payload(self) -> dict:
        p = Profile(name="default", dns="1.1.1.1", command="", domains=["example.com"])
        s = Settings(default_profile="default")
        return {
            "profiles": [p.to_dict()],
            "settings": s.to_dict(),
        }

    def load_all(self) -> tuple[list[Profile], Settings]:
        data = self.repo.read(self.path, default=self.default_payload())
        profiles = [Profile.from_dict(x) for x in data.get("profiles", [])]
        if not profiles:
            profiles = [Profile(name="default")]
        settings = Settings.from_dict(data.get("settings", {}))
        return profiles, settings

    def save_all(self, profiles: list[Profile], settings: Settings) -> None:
        data = {
            "profiles": [p.to_dict() for p in profiles],
            "settings": settings.to_dict(),
        }
        self.repo.write(self.path, data)

    def export_config(self, target: str | Path, profiles: list[Profile], settings: Settings) -> None:
        data = {
            "profiles": [p.to_dict() for p in profiles],
            "settings": settings.to_dict(),
        }
        self.repo.write(target, data)

    def import_config(self, source: str | Path) -> tuple[list[Profile], Settings]:
        data = self.repo.read(source, default=self.default_payload())
        profiles = [Profile.from_dict(x) for x in data.get("profiles", [])]
        settings = Settings.from_dict(data.get("settings", {}))
        return profiles, settings
