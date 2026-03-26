from app.models.profile import Profile


class ProfileService:
    def __init__(self, profiles: list[Profile] | None = None):
        self._profiles = profiles[:] if profiles else []

    def get_all(self) -> list[Profile]:
        return self._profiles[:]

    def set_all(self, profiles: list[Profile]) -> None:
        self._profiles = profiles[:]

    def exists(self, name: str) -> bool:
        return any(p.name == name for p in self._profiles)

    def get_by_name(self, name: str) -> Profile | None:
        for p in self._profiles:
            if p.name == name:
                return p
        return None

    def add(self, profile: Profile) -> None:
        ok, msg = profile.validate(require_command=False)
        if not ok:
            raise ValueError(msg)
        if self.exists(profile.name):
            raise ValueError("profile with this name already exists")
        self._profiles.append(profile)

    def update(self, old_name: str, profile: Profile) -> None:
        ok, msg = profile.validate(require_command=False)
        if not ok:
            raise ValueError(msg)
        for i, p in enumerate(self._profiles):
            if p.name == old_name:
                if profile.name != old_name and self.exists(profile.name):
                    raise ValueError("profile with this name already exists")
                self._profiles[i] = profile
                return
        raise ValueError("profile not found")

    def delete(self, name: str) -> None:
        for i, p in enumerate(self._profiles):
            if p.name == name:
                del self._profiles[i]
                return
        raise ValueError("profile not found")
