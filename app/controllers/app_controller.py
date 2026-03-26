from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from app.core.constants import STATUS_STOPPED
from app.core.signals import AppSignals
from app.models.app_state import AppState
from app.services.config_service import ConfigService
from app.services.log_service import LogService
from app.services.process_service import ProcessService
from app.services.profile_service import ProfileService
from app.services.tray_service import TrayService
from app.storage.json_repository import JsonRepository
from app.ui.main_window import MainWindow
from app.ui.styles import DARK_QSS, LIGHT_QSS


class AppController(MainWindow):
    def __init__(self):
        super().__init__()
        self.signals = AppSignals()
        self.state = AppState()
        self.log_service = LogService()
        self.config_service = ConfigService(JsonRepository())
        payload = self.config_service.load()
        self.profile_service = ProfileService(payload['profiles'])
        self.settings = payload['settings']
        self.process_service = ProcessService()

        self.tray = TrayService(
            self,
            on_show=self.showNormal,
            on_start=self.start_process,
            on_stop=self.stop_process,
            on_quit=QApplication.quit,
        )

        self._build_toolbar()
        self._bind_ui()
        self._apply_settings_to_ui()
        self._apply_theme()
        self.resize(self.settings.window_width, self.settings.window_height)
        self._refresh_profiles_page()
        self._set_status(STATUS_STOPPED)
        self._log('info', 'приложение запущено')

    def _build_toolbar(self):
        self.a_start = QAction('старт', self)
        self.a_stop = QAction('стоп', self)
        self.a_restart = QAction('рестарт', self)
        self.a_save = QAction('сохранить', self)
        self.a_import = QAction('импорт', self)
        self.a_export = QAction('экспорт', self)

        self.toolbar.addAction(self.a_start)
        self.toolbar.addAction(self.a_stop)
        self.toolbar.addAction(self.a_restart)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.a_save)
        self.toolbar.addAction(self.a_import)
        self.toolbar.addAction(self.a_export)

    def _bind_ui(self):
        self.a_start.triggered.connect(self.start_process)
        self.a_stop.triggered.connect(self.stop_process)
        self.a_restart.triggered.connect(self.restart_process)
        self.a_save.triggered.connect(self.save_all)
        self.a_import.triggered.connect(self.import_config)
        self.a_export.triggered.connect(self.export_config)

        self.dashboard_page.start_btn.clicked.connect(self.start_process)
        self.dashboard_page.stop_btn.clicked.connect(self.stop_process)
        self.dashboard_page.restart_btn.clicked.connect(self.restart_process)

        self.logs_page.clear_btn.clicked.connect(self.clear_logs)
        self.logs_page.save_btn.clicked.connect(self.save_log_to_file)

        self.settings_page.save_btn.clicked.connect(self.save_settings)

        self.profiles_page.table.itemSelectionChanged.connect(self.on_profile_selected)
        self.profiles_page.add_btn.clicked.connect(self.add_profile)
        self.profiles_page.remove_btn.clicked.connect(self.remove_profile)
        self.profiles_page.save_btn.clicked.connect(self.save_profile)

    def _apply_theme(self):
        self.setStyleSheet(DARK_QSS if self.settings.theme == 'dark' else LIGHT_QSS)

    def _apply_settings_to_ui(self):
        names = [x.name for x in self.profile_service.all()]
        self.settings_page.set_data(self.settings.to_dict(), names)

    def _refresh_profiles_page(self):
        self.profiles_page.fill([x.to_dict() for x in self.profile_service.all()])
        self.on_profile_selected()

    def _current_profile(self):
        row = self.profiles_page.current_row()
        items = self.profile_service.all()
        if 0 <= row < len(items):
            return items[row]

        x = self.profile_service.get(self.settings.default_profile)
        return x or (items[0] if items else None)

    def on_profile_selected(self):
        p = self._current_profile()
        if not p:
            return
        self.profiles_page.form.set_data(p.to_dict())
        self.dashboard_page.set_profile(p.name)
        self.dashboard_page.set_interface(p.interface or '-')
        self.dashboard_page.set_dns(p.dns or '-')

    def _set_status(self, status: str):
        self.state.status = status
        self.dashboard_page.set_status(status)
        self.tray.icon.setToolTip(f'net control: {status}')

    def _set_pid(self, pid: int):
        self.state.pid = pid

    def _log(self, level: str, text: str):
        line = self.log_service.add(level, text)
        self.logs_page.viewer.add_line(line)
        self.dashboard_page.add_event(line)

    def start_process(self):
        p = self._current_profile()
        if not p:
            QMessageBox.warning(self, 'ошибка', 'нет профиля')
            return
        ok = self.process_service.start(p, self._on_proc_line, self._on_proc_status, self._set_pid)
        if not ok:
            self._log('warning', 'процесс уже запущен')

    def stop_process(self):
        self.process_service.stop()

    def restart_process(self):
        p = self._current_profile()
        if not p:
            return
        self.process_service.restart(p, self._on_proc_line, self._on_proc_status, self._set_pid)

    def _on_proc_line(self, text: str):
        self._log('info', text)

    def _on_proc_status(self, status: str):
        self._set_status(status)
        self._log('info', f'статус: {status}')

    def save_profile(self):
        row = self.profiles_page.current_row()
        items = self.profile_service.all()
        if row < 0 or row >= len(items):
            return

        old_name = items[row].name
        data = self.profiles_page.form.get_data()
        try:
            from app.controllers.profile_controller import ProfileController
            ProfileController(self.profile_service).update(old_name, data)
            self._refresh_profiles_page()
            self._log('info', 'профиль сохранен')
            if self.settings.auto_save:
                self.save_all()
        except Exception as e:
            QMessageBox.critical(self, 'ошибка', str(e))

    def add_profile(self):
        name = f'profile_{len(self.profile_service.all()) + 1}'
        data = {
            'name': name,
            'interface': '',
            'dns': '1.1.1.1',
            'mode': 'normal',
            'timeout': 30,
            'autostart': False,
            'command': '',
            'domains': [],
        }
        try:
            from app.controllers.profile_controller import ProfileController
            ProfileController(self.profile_service).add(data)
            self._refresh_profiles_page()
            self._log('info', f'профиль создан: {name}')
            if self.settings.auto_save:
                self.save_all()
        except Exception as e:
            QMessageBox.critical(self, 'ошибка', str(e))

    def remove_profile(self):
        p = self._current_profile()
        if not p:
            return
        from app.controllers.profile_controller import ProfileController
        ProfileController(self.profile_service).remove(p.name)
        self._refresh_profiles_page()
        self._log('warning', f'профиль удален: {p.name}')
        if self.settings.auto_save:
            self.save_all()

    def save_settings(self):
        from app.controllers.settings_controller import SettingsController
        self.settings = SettingsController().build(self.settings_page.get_data() | {
            'window_width': self.width(),
            'window_height': self.height(),
        })
        self._apply_theme()
        self.save_all()
        self._log('info', 'настройки сохранены')

    def save_all(self):
        self.config_service.save(self.profile_service.all(), self.settings)
        self._apply_settings_to_ui()
        self._log('info', 'конфиг сохранен')

    def import_config(self):
        path, _ = QFileDialog.getOpenFileName(self, 'импорт', '', 'json files (*.json)')
        if not path:
            return
        try:
            payload = self.config_service.import_from(Path(path))
            self.profile_service.set_profiles(payload['profiles'])
            self.settings = payload['settings']
            self._apply_settings_to_ui()
            self._apply_theme()
            self._refresh_profiles_page()
            self._log('info', f'конфиг импортирован: {path}')
        except Exception as e:
            QMessageBox.critical(self, 'ошибка', str(e))

    def export_config(self):
        path, _ = QFileDialog.getSaveFileName(self, 'экспорт', 'config.json', 'json files (*.json)')
        if not path:
            return
        self.config_service.export_to(Path(path), self.profile_service.all(), self.settings)
        self._log('info', f'конфиг экспортирован: {path}')

    def clear_logs(self):
        self.log_service.clear()
        self.logs_page.viewer.clear()
        self.dashboard_page.events.clear()

    def save_log_to_file(self):
        path, _ = QFileDialog.getSaveFileName(self, 'сохранить лог', 'app.log', 'log files (*.log *.txt)')
        if not path:
            return
        Path(path).write_text('\n'.join(self.log_service.all()), encoding='utf-8')
        self._log('info', f'лог сохранен: {path}')

    def closeEvent(self, e):
        self.settings.window_width = self.width()
        self.settings.window_height = self.height()
        if self.settings.to_tray:
            e.ignore()
            self.hide()
            self._log('info', 'окно свернуто в трей')
        else:
            self.stop_process()
            self.save_all()
            e.accept()
