from dataclasses import dataclass

from app.core.constants import STATUS_STOPPED


@dataclass
class AppState:
    status: str = STATUS_STOPPED
    active_profile: str = ""
    last_log: str = ""
    is_process_running: bool = False
