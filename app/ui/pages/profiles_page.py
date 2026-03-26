from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from app.ui.widgets.profile_form import ProfileForm


class ProfilesPage(QWidget):
    def __init__(self):
        super().__init__()
        root = QHBoxLayout(self)

        left = QVBoxLayout()
        left.addWidget(QLabel('профили'))

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['имя', 'интерфейс', 'dns', 'режим'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        left.addWidget(self.table)

        h = QHBoxLayout()
        self.add_btn = QPushButton('добавить')
        self.remove_btn = QPushButton('удалить')
        self.save_btn = QPushButton('сохранить')
        h.addWidget(self.add_btn)
        h.addWidget(self.remove_btn)
        h.addWidget(self.save_btn)
        left.addLayout(h)

        self.form = ProfileForm()

        l = QWidget()
        l.setLayout(left)
        root.addWidget(l, 3)
        root.addWidget(self.form, 2)

    def fill(self, profiles: list[dict]):
        self.table.setRowCount(0)
        for p in profiles:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(p.get('name', '')))
            self.table.setItem(r, 1, QTableWidgetItem(p.get('interface', '')))
            self.table.setItem(r, 2, QTableWidgetItem(p.get('dns', '')))
            self.table.setItem(r, 3, QTableWidgetItem(p.get('mode', '')))

        if self.table.rowCount():
            self.table.selectRow(0)

    def current_row(self):
        return self.table.currentRow()
