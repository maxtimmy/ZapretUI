from PySide6.QtWidgets import QMainWindow, QStackedWidget, QToolBar, QWidget, QHBoxLayout

from app.core.constants import PAGE_DASHBOARD, PAGE_LOGS, PAGE_PROFILES, PAGE_SETTINGS
from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.logs_page import LogsPage
from app.ui.pages.profiles_page import ProfilesPage
from app.ui.pages.settings_page import SettingsPage
from app.ui.widgets.side_menu import SideMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('net control')

        c = QWidget()
        self.setCentralWidget(c)
        root = QHBoxLayout(c)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        self.menu = SideMenu([PAGE_DASHBOARD, PAGE_PROFILES, PAGE_LOGS, PAGE_SETTINGS])
        self.stack = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.profiles_page = ProfilesPage()
        self.logs_page = LogsPage()
        self.settings_page = SettingsPage()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.profiles_page)
        self.stack.addWidget(self.logs_page)
        self.stack.addWidget(self.settings_page)

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)

        root.addWidget(self.menu)
        root.addWidget(self.stack, 1)

        self.toolbar = QToolBar('main')
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)
