from dataclasses import dataclass


@dataclass
class Settings:
    default_profile: str = 'default'
    theme: str = 'dark'
    to_tray: bool = True
    auto_save: bool = True
    window_width: int = 1280
    window_height: int = 820

    def to_dict(self):
        return {
            'default_profile': self.default_profile,
            'theme': self.theme,
            'to_tray': self.to_tray,
            'auto_save': self.auto_save,
            'window_width': self.window_width,
            'window_height': self.window_height,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            default_profile=d.get('default_profile', 'default'),
            theme=d.get('theme', 'dark'),
            to_tray=bool(d.get('to_tray', True)),
            auto_save=bool(d.get('auto_save', True)),
            window_width=int(d.get('window_width', 1280)),
            window_height=int(d.get('window_height', 820)),
        )
