from PySide6.QtWidgets import QMenu, QSystemTrayIcon


class TrayService:
    def __init__(self, parent, on_show, on_start, on_stop, on_quit):
        self.icon = QSystemTrayIcon(parent)
        self.icon.setToolTip('net control')

        m = QMenu()
        a1 = m.addAction('показать')
        a2 = m.addAction('старт')
        a3 = m.addAction('стоп')
        m.addSeparator()
        a4 = m.addAction('выход')

        a1.triggered.connect(on_show)
        a2.triggered.connect(on_start)
        a3.triggered.connect(on_stop)
        a4.triggered.connect(on_quit)

        self.icon.setContextMenu(m)
        self.icon.show()
