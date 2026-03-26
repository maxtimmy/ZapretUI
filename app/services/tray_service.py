from PySide6.QtWidgets import QMenu, QSystemTrayIcon


class TrayService:
    def __init__(self, parent, on_show, on_start, on_stop, on_exit):
        self.icon = QSystemTrayIcon(parent)
        self.icon.setToolTip("Net Control")

        m = QMenu()
        a1 = m.addAction("show")
        a2 = m.addAction("start")
        a3 = m.addAction("stop")
        m.addSeparator()
        a4 = m.addAction("exit")

        a1.triggered.connect(on_show)
        a2.triggered.connect(on_start)
        a3.triggered.connect(on_stop)
        a4.triggered.connect(on_exit)

        self.icon.setContextMenu(m)
        self.icon.show()
