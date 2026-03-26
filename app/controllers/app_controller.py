from PySide6.QtWidgets import QFileDialog, QMessageBox

from app.core.config import APP_NAME
from app.models.app_state import AppState
from app.services.config_service import ConfigService
from app.services.log_service import LogService
from app.services.process_service import ProcessService
from app.services.profile_service import ProfileService
from app.ui.main_window import MainWindow
from app.ui.styles import get_style
from .profile_controller import ProfileController
from .settings_controller import SettingsController
from .process_controller import ProcessController


class AppController:
    def __init__(self, app):
        self.app = app
        self.state = AppState()

        self.config_service = ConfigService()
        profiles, settings = self.config_service.load_all()
        self.settings = settings

        self.log_service = LogService()
        self.profile_service = ProfileService(profiles)
        self.process_service = ProcessService()

        self.window = MainWindow(APP_NAME)
        self.window.resize(self.settings.window_width, self.settings.window_height)

        self.profile_controller = ProfileController(
            self.profile_service,
            self.config_service,
            self.settings,
            self.log_service,
            self.window.profiles_page,
        )
        self.settings_controller = SettingsController(
            self.settings,
            self.config_service,
            self.profile_service,
            self.window.settings_page,
            self.apply_theme,
            self.log_service,
        )
        self.process_controller = ProcessController(
            self.process_service,
            self.profile_service,
            self.settings,
            self.log_service,
            self.update_ui,
        )

        self._bind()
        self.profile_controller.refresh()
        self.settings_controller.refresh()
        self.apply_theme(self.settings.theme)
        self.window.dashboard_page.set_recent_logs(self.log_service.get_all())
        self.window.logs_page.set_logs(self.log_service.get_all())
        self.on_profile_selected()
        self._update_action_states()

    def _bind(self):
        self.window.start_requested.connect(self._safe_start)
        self.window.stop_requested.connect(self._safe_stop)
        self.window.restart_requested.connect(self._safe_restart)

        self.window.profiles_page.add_requested.connect(self._safe_add_profile)
        self.window.profiles_page.save_requested.connect(self._safe_save_profile)
        self.window.profiles_page.delete_requested.connect(self._safe_delete_profile)
        self.window.profiles_page.selection_changed.connect(self.on_profile_selected)
        self.window.profiles_page.form_changed.connect(self._update_action_states)

        self.window.settings_page.save_requested.connect(self._safe_save_settings)
        self.window.logs_page.save_requested.connect(self.save_logs)
        self.window.logs_page.clear_requested.connect(self.clear_logs)

        self.window.import_requested.connect(self.import_config)
        self.window.export_requested.connect(self.export_config)

    def show(self):
        self.window.show()

    def apply_theme(self, theme: str):
        self.app.setStyleSheet(get_style(theme))

    def update_ui(self, *, status=None, log=None, profile=None):
        if status is not None:
            self.state.status = status
            self.state.is_process_running = status == "running"
            self.window.set_status(status)

        if log is not None:
            self.state.last_log = log
            self.window.append_log(log)

        if profile is not None:
            self.state.active_profile = profile.name
            self.window.set_profile(profile)

        self._update_action_states()

    def on_profile_selected(self):
        p = self.window.profiles_page.selected_profile_obj()
        if p:
            self.window.dashboard_page.set_profile_info(p)
        self._update_action_states()

    def _update_action_states(self):
        p = self.window.profiles_page.selected_profile_obj()
        status = (self.state.status or "").strip().lower()

        has_profile = p is not None
        has_command = bool(p and p.command.strip())

        start_enabled = False
        restart_enabled = False
        stop_enabled = False

        start_reason = ""
        restart_reason = ""
        stop_reason = ""

        if not has_profile:
            start_reason = "no profile selected"
            restart_reason = "no profile selected"
            stop_reason = "process is not running"

        elif not has_command:
            start_reason = "command is empty"
            restart_reason = "command is empty"
            stop_reason = "process is not running"

        else:
            if status in ("starting", "stopping", "restarting"):
                start_reason = f"process is {status}"
                restart_reason = f"process is {status}"
                stop_reason = f"process is {status}"

            elif status == "running":
                start_reason = "process already running"
                start_enabled = False

                restart_enabled = True
                stop_enabled = True

            else:
                start_enabled = True
                restart_enabled = True
                stop_reason = "process is not running"

        self.window.set_start_enabled(start_enabled, start_reason)
        self.window.set_restart_enabled(restart_enabled, restart_reason)
        self.window.set_stop_enabled(stop_enabled, stop_reason)

    def _safe_start(self):
        try:
            self.update_ui(status="starting")
            self.process_controller.start()
        except Exception as e:
            self.update_ui(status="error")
            QMessageBox.warning(self.window, "error", str(e))

    def _safe_stop(self):
        try:
            self.update_ui(status="stopping")
            self.process_controller.stop()
        except Exception as e:
            self.update_ui(status="error")
            QMessageBox.warning(self.window, "error", str(e))

    def _safe_restart(self):
        try:
            self.update_ui(status="restarting")
            self.process_controller.restart()
        except Exception as e:
            self.update_ui(status="error")
            QMessageBox.warning(self.window, "error", str(e))

    def _safe_add_profile(self):
        try:
            self.profile_controller.add_profile()
            self.settings_controller.refresh()
            self.window.append_log("profile added")
            self._update_action_states()
        except Exception as e:
            QMessageBox.warning(self.window, "error", str(e))

    def _safe_save_profile(self):
        try:
            self.profile_controller.save_selected()
            self.settings_controller.refresh()
            self.window.logs_page.set_logs(self.log_service.get_all())
            self._update_action_states()
        except Exception as e:
            QMessageBox.warning(self.window, "error", str(e))

    def _safe_delete_profile(self):
        try:
            self.profile_controller.delete_selected()
            self.settings_controller.refresh()
            self.window.logs_page.set_logs(self.log_service.get_all())
            self._update_action_states()
        except Exception as e:
            QMessageBox.warning(self.window, "error", str(e))

    def _safe_save_settings(self):
        try:
            self.settings = self.settings_controller.save()
            self.process_controller.settings = self.settings
        except Exception as e:
            QMessageBox.warning(self.window, "error", str(e))

    def save_logs(self):
        path, _ = QFileDialog.getSaveFileName(self.window, "save log", "app.log", "Log (*.log *.txt)")
        if path:
            self.log_service.save_to_file(path)

    def clear_logs(self):
        self.log_service.clear()
        self.window.logs_page.clear_logs()
        self.window.dashboard_page.set_recent_logs([])

    def import_config(self):
        path, _ = QFileDialog.getOpenFileName(self.window, "import config", "", "JSON (*.json)")
        if not path:
            return

        try:
            profiles, settings = self.config_service.import_config(path)
            self.profile_service.set_all(profiles)
            self.settings = settings
            self.process_controller.settings = settings
            self.profile_controller.settings = settings
            self.settings_controller.settings = settings

            self.profile_controller.refresh()
            self.settings_controller.refresh()
            self.apply_theme(settings.theme)
            self.window.append_log(f"config imported: {path}")
            self.on_profile_selected()
            self._update_action_states()
        except Exception as e:
            QMessageBox.warning(self.window, "error", str(e))

    def export_config(self):
        path, _ = QFileDialog.getSaveFileName(self.window, "export config", "config.json", "JSON (*.json)")
        if not path:
            return

        try:
            self.config_service.export_config(path, self.profile_service.get_all(), self.settings)
            self.window.append_log(f"config exported: {path}")
        except Exception as e:
            QMessageBox.warning(self.window, "error", str(e))