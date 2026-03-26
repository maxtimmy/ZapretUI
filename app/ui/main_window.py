from PySide6.QtCore import Signal, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QToolButton

from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.profiles_page import ProfilesPage
from app.ui.pages.logs_page import LogsPage
from app.ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):
    start_requested = Signal()
    stop_requested = Signal()
    restart_requested = Signal()
    import_requested = Signal()
    export_requested = Signal()

    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)

        self.dashboard_page = DashboardPage()
        self.profiles_page = ProfilesPage()
        self.logs_page = LogsPage()
        self.settings_page = SettingsPage()

        self.nav = QListWidget()
        self.nav.addItems(["dashboard", "profiles", "logs", "settings"])
        self.nav.setFixedWidth(170)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.profiles_page)
        self.stack.addWidget(self.logs_page)
        self.stack.addWidget(self.settings_page)

        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0)

        c = QWidget()
        self.setCentralWidget(c)
        root = QHBoxLayout(c)
        root.addWidget(self.nav)
        root.addWidget(self.stack, 1)

        self._make_toolbar()

        self.dashboard_page.start_btn.clicked.connect(self.start_requested.emit)
        self.dashboard_page.stop_btn.clicked.connect(self.stop_requested.emit)
        self.dashboard_page.restart_btn.clicked.connect(self.restart_requested.emit)

        self._busy_mode = None
        self._busy_step = 0
        self._busy_timer = QTimer(self)
        self._busy_timer.timeout.connect(self._tick_busy)

        self._start_text = "start"
        self._stop_text = "stop"
        self._restart_text = "restart"

    def _make_toolbar(self):
        tb = self.addToolBar("main")
        tb.setMovable(False)

        self.start_action = QAction("start", self)
        self.stop_action = QAction("stop", self)
        self.restart_action = QAction("restart", self)
        self.import_action = QAction("import", self)
        self.export_action = QAction("export", self)

        self.start_action.triggered.connect(self.start_requested.emit)
        self.stop_action.triggered.connect(self.stop_requested.emit)
        self.restart_action.triggered.connect(self.restart_requested.emit)
        self.import_action.triggered.connect(self.import_requested.emit)
        self.export_action.triggered.connect(self.export_requested.emit)

        tb.addAction(self.start_action)
        tb.addAction(self.stop_action)
        tb.addAction(self.restart_action)
        tb.addSeparator()
        tb.addAction(self.import_action)
        tb.addAction(self.export_action)

        self.start_tool_btn = tb.widgetForAction(self.start_action)
        self.stop_tool_btn = tb.widgetForAction(self.stop_action)
        self.restart_tool_btn = tb.widgetForAction(self.restart_action)

        for b in [self.start_tool_btn, self.stop_tool_btn, self.restart_tool_btn]:
            if isinstance(b, QToolButton):
                b.setToolButtonStyle(b.toolButtonStyle())

    def _set_toolbar_text(self, action, text: str):
        action.setText(text)
        btn = None
        if action is self.start_action:
            btn = self.start_tool_btn
        elif action is self.stop_action:
            btn = self.stop_tool_btn
        elif action is self.restart_action:
            btn = self.restart_tool_btn

        if btn:
            btn.setText(text)

    def _busy_frames(self, base: str):
        return [f"{base}.", f"{base}..", f"{base}..."]

    def _tick_busy(self):
        if not self._busy_mode:
            return

        frames = self._busy_frames(self._busy_mode)
        txt = frames[self._busy_step % len(frames)]
        self._busy_step += 1

        if self._busy_mode == "starting":
            self.dashboard_page.start_btn.setText(txt)
            self._set_toolbar_text(self.start_action, txt)
        elif self._busy_mode == "stopping":
            self.dashboard_page.stop_btn.setText(txt)
            self._set_toolbar_text(self.stop_action, txt)
        elif self._busy_mode == "restarting":
            self.dashboard_page.restart_btn.setText(txt)
            self._set_toolbar_text(self.restart_action, txt)

    def set_busy_state(self, mode: str | None):
        self._busy_mode = mode
        self._busy_step = 0

        self.dashboard_page.start_btn.setText(self._start_text)
        self.dashboard_page.stop_btn.setText(self._stop_text)
        self.dashboard_page.restart_btn.setText(self._restart_text)

        self._set_toolbar_text(self.start_action, self._start_text)
        self._set_toolbar_text(self.stop_action, self._stop_text)
        self._set_toolbar_text(self.restart_action, self._restart_text)

        if mode:
            self._busy_timer.start(250)
            self._tick_busy()
        else:
            self._busy_timer.stop()

    def set_status(self, status: str):
        self.dashboard_page.set_status(status)
        self.statusBar().showMessage(status)

        s = (status or "").strip().lower()
        if s == "starting":
            self.set_busy_state("starting")
        elif s == "stopping":
            self.set_busy_state("stopping")
        elif s == "restarting":
            self.set_busy_state("restarting")
        else:
            self.set_busy_state(None)

    def set_profile(self, profile):
        self.dashboard_page.set_profile_info(profile)

    def append_log(self, text: str):
        self.logs_page.append_log(text)
        self.dashboard_page.append_event(text)

    def set_start_enabled(self, enabled: bool, reason: str = ""):
        self.dashboard_page.start_btn.set_disabled_hint(reason)
        self.dashboard_page.start_btn.setEnabled(enabled)

        self.start_action.setEnabled(enabled)
        if self.start_tool_btn:
            self.start_tool_btn.setToolTip("" if enabled else reason)

    def set_restart_enabled(self, enabled: bool, reason: str = ""):
        self.dashboard_page.restart_btn.set_disabled_hint(reason)
        self.dashboard_page.restart_btn.setEnabled(enabled)

        self.restart_action.setEnabled(enabled)
        if self.restart_tool_btn:
            self.restart_tool_btn.setToolTip("" if enabled else reason)

    def set_stop_enabled(self, enabled: bool, reason: str = ""):
        self.dashboard_page.stop_btn.set_disabled_hint(reason)
        self.dashboard_page.stop_btn