class SettingsController:
    def __init__(self, settings, config_service, profile_service, page, style_cb, log_service):
        self.settings = settings
        self.config_service = config_service
        self.profile_service = profile_service
        self.page = page
        self.style_cb = style_cb
        self.log_service = log_service

    def refresh(self):
        self.page.set_data(self.settings, [p.name for p in self.profile_service.get_all()])

    def save(self):
        self.settings = self.page.read_data()
        self.config_service.save_all(self.profile_service.get_all(), self.settings)
        self.style_cb(self.settings.theme)
        self.log_service.info("settings saved")
        return self.settings
