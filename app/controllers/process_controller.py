class ProcessController:
    def __init__(self, process_service, profile_service, settings, log_service, ui_callback):
        self.process_service = process_service
        self.profile_service = profile_service
        self.settings = settings
        self.log_service = log_service
        self.ui_callback = ui_callback

        self.process_service.set_callbacks(self.on_process_log, self.on_process_status)

    def _active_profile(self):
        p = self.profile_service.get_by_name(self.settings.default_profile)
        if p:
            return p
        items = self.profile_service.get_all()
        return items[0] if items else None

    def start(self):
        p = self._active_profile()
        if not p:
            raise ValueError("no profile")
        self.process_service.start(p)
        self.ui_callback(profile=p)

    def stop(self):
        self.process_service.stop()

    def restart(self):
        p = self._active_profile()
        if not p:
            raise ValueError("no profile")
        self.process_service.restart(p)
        self.ui_callback(profile=p)

    def on_process_log(self, line: str):
        self.log_service.info(line)
        self.ui_callback(log=line)

    def on_process_status(self, status: str):
        self.ui_callback(status=status)
