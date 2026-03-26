from PySide6.QtCore import QObject, Signal


class AppSignals(QObject):
    log_added = Signal(str, str)
    status_changed = Signal(str)
    profiles_changed = Signal()
    settings_changed = Signal()
