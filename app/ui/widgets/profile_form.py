from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)


class ProfileForm(QWidget):
    def __init__(self):
        super().__init__()
        f = QFormLayout(self)

        self.name_edit = QLineEdit()
        self.interface_edit = QLineEdit()
        self.dns_edit = QLineEdit()
        self.mode_box = QComboBox()
        self.mode_box.addItems(['normal', 'debug', 'custom'])
        self.timeout_box = QSpinBox()
        self.timeout_box.setRange(1, 99999)
        self.timeout_box.setValue(30)
        self.autostart_box = QCheckBox('автозапуск')
        self.command_edit = QLineEdit()

        self.domains_table = QTableWidget(0, 1)
        self.domains_table.setHorizontalHeaderLabels(['домен'])
        self.domains_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.domains_table.verticalHeader().setVisible(False)

        a = QPushButton('добавить домен')
        b = QPushButton('удалить домен')
        a.clicked.connect(self.add_domain)
        b.clicked.connect(self.del_domain)

        h = QHBoxLayout()
        h.addWidget(a)
        h.addWidget(b)

        f.addRow('имя', self.name_edit)
        f.addRow('интерфейс', self.interface_edit)
        f.addRow('dns', self.dns_edit)
        f.addRow('режим', self.mode_box)
        f.addRow('таймаут', self.timeout_box)
        f.addRow('', self.autostart_box)
        f.addRow('команда', self.command_edit)
        f.addRow(self.domains_table)
        f.addRow(h)

    def add_domain(self):
        r = self.domains_table.rowCount()
        self.domains_table.insertRow(r)
        self.domains_table.setItem(r, 0, QTableWidgetItem('example.com'))

    def del_domain(self):
        r = self.domains_table.currentRow()
        if r >= 0:
            self.domains_table.removeRow(r)

    def set_data(self, data: dict):
        self.name_edit.setText(data.get('name', ''))
        self.interface_edit.setText(data.get('interface', ''))
        self.dns_edit.setText(data.get('dns', ''))
        self.mode_box.setCurrentText(data.get('mode', 'normal'))
        self.timeout_box.setValue(int(data.get('timeout', 30)))
        self.autostart_box.setChecked(bool(data.get('autostart', False)))
        self.command_edit.setText(data.get('command', ''))

        self.domains_table.setRowCount(0)
        for x in data.get('domains', []):
            r = self.domains_table.rowCount()
            self.domains_table.insertRow(r)
            self.domains_table.setItem(r, 0, QTableWidgetItem(x))

    def get_data(self):
        domains = []
        for r in range(self.domains_table.rowCount()):
            it = self.domains_table.item(r, 0)
            if it and it.text().strip():
                domains.append(it.text().strip())

        return {
            'name': self.name_edit.text().strip(),
            'interface': self.interface_edit.text().strip(),
            'dns': self.dns_edit.text().strip(),
            'mode': self.mode_box.currentText(),
            'timeout': self.timeout_box.value(),
            'autostart': self.autostart_box.isChecked(),
            'command': self.command_edit.text().strip(),
            'domains': domains,
        }
