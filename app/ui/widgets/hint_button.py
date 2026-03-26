from PySide6.QtWidgets import QPushButton


class HintButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._disabled_hint = ""

    def set_disabled_hint(self, text: str):
        self._disabled_hint = text or ""
        self._update_tooltip()

    def setEnabled(self, enabled: bool):
        super().setEnabled(enabled)
        self._update_tooltip()

    def _update_tooltip(self):
        if self.isEnabled():
            self.setToolTip("")
        else:
            self.setToolTip(self._disabled_hint)