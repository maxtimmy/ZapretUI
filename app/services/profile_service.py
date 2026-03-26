from app.models.profile import Profile


class ProfileService:
    def __init__(self, profiles: list[Profile] | None = None):
        self._profiles = profiles or []

    def set_profiles(self, items: list[Profile]):
        self._profiles = items

    def all(self):
        return list(self._profiles)

    def get(self, name: str):
        for x in self._profiles:
            if x.name == name:
                return x
        return None

    def add(self, p: Profile):
        p.validate()
        if self.get(p.name):
            raise ValueError('профиль с таким именем уже есть')
        self._profiles.append(p)

    def update(self, old_name: str, p: Profile):
        p.validate()
        for i, x in enumerate(self._profiles):
            if x.name == old_name:
                if old_name != p.name and self.get(p.name):
                    raise ValueError('профиль с таким именем уже есть')
                self._profiles[i] = p
                return
        raise ValueError('профиль не найден')

    def remove(self, name: str):
        self._profiles = [x for x in self._profiles if x.name != name]
