from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QComboBox, QSpinBox,
    QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QHBoxLayout, QLabel, QVBoxLayout
)

from app.models.profile import Profile


class ProfileForm(QWidget):
    changed = Signal()

    def __init__(self):
        super().__init__()

        self.name_edit = QLineEdit()
        self.iface_edit = QLineEdit()
        self.dns_edit = QLineEdit()
        self.mode_box = QComboBox()
        self.mode_box.addItems(["normal", "debug", "custom"])
        self.timeout_box = QSpinBox()
        self.timeout_box.setRange(1, 99999)
        self.timeout_box.setValue(30)
        self.autostart_box = QCheckBox("autostart")
        self.command_edit = QLineEdit()

        self.domains = QTableWidget(0, 1)
        self.domains.setHorizontalHeaderLabels(["domain"])
        self.domains.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.domains.verticalHeader().setVisible(False)

        a = QPushButton("add domain")
        b = QPushButton("delete domain")
        a.clicked.connect(self.add_domain)
        b.clicked.connect(self.delete_domain)

        btns = QHBoxLayout()
        btns.addWidget(a)
        btns.addWidget(b)

        form = QFormLayout()
        form.addRow("name", self.name_edit)
        form.addRow("interface", self.iface_edit)
        form.addRow("dns", self.dns_edit)
        form.addRow("mode", self.mode_box)
        form.addRow("timeout", self.timeout_box)
        form.addRow("", self.autostart_box)
        form.addRow("command", self.command_edit)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addWidget(QLabel("domains"))
        root.addWidget(self.domains)
        root.addLayout(btns)

        self._bind()

    def _bind(self):
        self.name_edit.textChanged.connect(self.changed.emit)
        self.iface_edit.textChanged.connect(self.changed.emit)
        self.dns_edit.textChanged.connect(self.changed.emit)
        self.mode_box.currentIndexChanged.connect(self.changed.emit)
        self.timeout_box.valueChanged.connect(self.changed.emit)
        self.autostart_box.stateChanged.connect(self.changed.emit)
        self.command_edit.textChanged.connect(self.changed.emit)

        self.domains.itemChanged.connect(lambda *_: self.changed.emit())
        self.domains.model().rowsInserted.connect(lambda *_: self.changed.emit())
        self.domains.model().rowsRemoved.connect(lambda *_: self.changed.emit())

    def add_domain(self):
        r = self.domains.rowCount()
        self.domains.insertRow(r)
        self.domains.setItem(r, 0, QTableWidgetItem("example.com"))
        self.changed.emit()

    def delete_domain(self):
        r = self.domains.currentRow()
        if r >= 0:
            self.domains.removeRow(r)
            self.changed.emit()

    def get_data(self) -> Profile:
        items = []
        for r in range(self.domains.rowCount()):
            it = self.domains.item(r, 0)
            if it and it.text().strip():
                items.append(it.text().strip())

        return Profile(
            name=self.name_edit.text().strip(),
            interface=self.iface_edit.text().strip(),
            dns=self.dns_edit.text().strip(),
            mode=self.mode_box.currentText(),
            timeout=self.timeout_box.value(),
            autostart=self.autostart_box.isChecked(),
            command=self.command_edit.text().strip(),
            domains=items,
        )

    def set_data(self, p: Profile):
        self.name_edit.setText(p.name)
        self.iface_edit.setText(p.interface)
        self.dns_edit.setText(p.dns)
        self.mode_box.setCurrentText(p.mode)
        self.timeout_box.setValue(p.timeout)
        self.autostart_box.setChecked(p.autostart)
        self.command_edit.setText(p.command)

        self.domains.blockSignals(True)
        self.domains.setRowCount(0)
        for x in p.domains:
            r = self.domains.rowCount()
            self.domains.insertRow(r)
            self.domains.setItem(r, 0, QTableWidgetItem(x))
        self.domains.blockSignals(False)

        self.changed.emit()

    def has_command(self) -> bool:
        return bool(self.command_edit.text().strip())