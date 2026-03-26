from app.models.profile import Profile


class ProfileController:
    def __init__(self, service, config_service, settings, log_service, page):
        self.service = service
        self.config_service = config_service
        self.settings = settings
        self.log_service = log_service
        self.page = page

    def refresh(self):
        self.page.set_profiles(self.service.get_all())

    def add_profile(self):
        p = Profile(name=f"profile_{len(self.service.get_all()) + 1}")
        self.service.add(p)
        self._save()
        self.refresh()
        self.log_service.info(f"profile created: {p.name}")

    def save_selected(self):
        old_name = self.page.current_profile_name()
        p = self.page.read_profile()
        if old_name:
            self.service.update(old_name, p)
        else:
            self.service.add(p)
        self._save()
        self.refresh()
        self.page.select_by_name(p.name)
        self.log_service.info(f"profile saved: {p.name}")

    def delete_selected(self):
        name = self.page.current_profile_name()
        if not name:
            return
        self.service.delete(name)
        self._save()
        self.refresh()
        self.log_service.warning(f"profile deleted: {name}")

    def _save(self):
        self.config_service.save_all(self.service.get_all(), self.settings)
