from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel
)

from app.models.profile import Profile
from app.ui.widgets.profile_form import ProfileForm


class ProfilesPage(QWidget):
    add_requested = Signal()
    save_requested = Signal()
    delete_requested = Signal()
    selection_changed = Signal()
    form_changed = Signal()

    def __init__(self):
        super().__init__()

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["name", "interface", "dns", "mode"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.itemSelectionChanged.connect(self._select_changed)

        self.form = ProfileForm()
        self.form.changed.connect(self.form_changed.emit)

        left = QVBoxLayout()
        left.addWidget(QLabel("profiles"))
        left.addWidget(self.table)

        self.add_btn = QPushButton("add")
        self.save_btn = QPushButton("save")
        self.delete_btn = QPushButton("delete")

        self.add_btn.clicked.connect(self.add_requested.emit)
        self.save_btn.clicked.connect(self.save_requested.emit)
        self.delete_btn.clicked.connect(self.delete_requested.emit)

        row = QHBoxLayout()
        row.addWidget(self.add_btn)
        row.addWidget(self.save_btn)
        row.addWidget(self.delete_btn)
        left.addLayout(row)

        root = QHBoxLayout(self)
        root.addLayout(left, 3)
        root.addWidget(self.form, 2)

        self._profiles: list[Profile] = []

    def set_profiles(self, profiles: list[Profile]):
        self._profiles = profiles[:]
        self.table.setRowCount(0)

        for p in profiles:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(p.name))
            self.table.setItem(r, 1, QTableWidgetItem(p.interface))
            self.table.setItem(r, 2, QTableWidgetItem(p.dns))
            self.table.setItem(r, 3, QTableWidgetItem(p.mode))

        if profiles:
            self.table.selectRow(0)
            self.form.set_data(profiles[0])
        else:
            self.form.set_data(Profile(name=""))

    def _select_changed(self):
        r = self.table.currentRow()
        if 0 <= r < len(self._profiles):
            self.form.set_data(self._profiles[r])
            self.selection_changed.emit()
        else:
            self.form.set_data(Profile(name=""))
            self.selection_changed.emit()

    def current_profile_name(self) -> str:
        r = self.table.currentRow()
        if 0 <= r < len(self._profiles):
            return self._profiles[r].name
        return ""

    def read_profile(self) -> Profile:
        return self.form.get_data()

    def selected_profile_obj(self) -> Profile | None:
        r = self.table.currentRow()
        if 0 <= r < len(self._profiles):
            return self._profiles[r]
        return None

    def select_by_name(self, name: str):
        for i, p in enumerate(self._profiles):
            if p.name == name:
                self.table.selectRow(i)
                self.form.set_data(p)
                return

    def has_command_in_form(self) -> bool:
        return self.form.has_command()