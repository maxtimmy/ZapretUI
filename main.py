import sys
from PySide6.QtWidgets import QApplication, QMessageBox

from app.controllers.app_controller import AppController


def main():
    app = QApplication(sys.argv)
    try:
        c = AppController(app)
        c.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "startup error", str(e))
        raise


if __name__ == "__main__":
    main()
