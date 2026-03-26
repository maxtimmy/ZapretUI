from app.models.app_state import AppState
from app.services.log_service import LogService
from app.services.process_service import ProcessService


class ProcessController:
    def __init__(self, process_service: ProcessService, log_service: LogService, state: AppState):
        self.process_service = process_service
        self.log_service = log_service
        self.state = state

    def start(self, profile, on_line, on_status, on_pid):
        return self.process_service.start(profile, on_line, on_status, on_pid)

    def stop(self):
        self.process_service.stop()

    def restart(self, profile, on_line, on_status, on_pid):
        return self.process_service.restart(profile, on_line, on_status, on_pid)
