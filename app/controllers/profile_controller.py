from app.models.profile import Profile
from app.services.profile_service import ProfileService


class ProfileController:
    def __init__(self, service: ProfileService):
        self.service = service

    def build_profile(self, data: dict):
        p = Profile.from_dict(data)
        p.validate()
        return p

    def add(self, data: dict):
        p = self.build_profile(data)
        self.service.add(p)

    def update(self, old_name: str, data: dict):
        p = self.build_profile(data)
        self.service.update(old_name, p)

    def remove(self, name: str):
        self.service.remove(name)
