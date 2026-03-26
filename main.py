import sys
from PySide6.QtWidgets import QApplication

from app.controllers.app_controller import AppController


def main():
    app = QApplication(sys.argv)
    c = AppController()
    c.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
