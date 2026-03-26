from PySide6.QtWidgets import QListWidget


class SideMenu(QListWidget):
    def __init__(self, items: list[str]):
        super().__init__()
        self.addItems(items)
        self.setFixedWidth(180)
        self.setCurrentRow(0)
