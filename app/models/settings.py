from dataclasses import dataclass

from app.core.config import DEFAULT_THEME
from app.core.constants import DEFAULT_PROFILE_NAME


@dataclass
class Settings:
    default_profile: str = DEFAULT_PROFILE_NAME
    theme: str = DEFAULT_THEME
    to_tray: bool = True
    auto_save: bool = True
    window_width: int = 1280
    window_height: int = 820

    def to_dict(self) -> dict:
        return {
            "default_profile": self.default_profile,
            "theme": self.theme,
            "to_tray": self.to_tray,
            "auto_save": self.auto_save,
            "window_width": self.window_width,
            "window_height": self.window_height,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Settings":
        return cls(
            default_profile=str(data.get("default_profile", DEFAULT_PROFILE_NAME)),
            theme=str(data.get("theme", DEFAULT_THEME)),
            to_tray=bool(data.get("to_tray", True)),
            auto_save=bool(data.get("auto_save", True)),
            window_width=int(data.get("window_width", 1280) or 1280),
            window_height=int(data.get("window_height", 820) or 820),
        )
