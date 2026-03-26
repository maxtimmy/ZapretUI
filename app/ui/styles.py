def get_dark_style() -> str:
    return """
    QWidget { background:#1f232a; color:#e8edf2; font-size:13px; }
    QMainWindow { background:#1f232a; }
    QPushButton { background:#2d333b; border:1px solid #444c56; border-radius:8px; padding:8px 12px; }
    QPushButton:hover { background:#373e47; }
    QLineEdit, QTextEdit, QComboBox, QSpinBox, QTableWidget, QListWidget { 
        background:#22272e; border:1px solid #444c56; border-radius:8px; padding:6px; 
    }
    QHeaderView::section { background:#2d333b; padding:6px; border:none; }
    QGroupBox { border:1px solid #444c56; border-radius:10px; margin-top:10px; padding-top:10px; }
    QGroupBox::title { subcontrol-origin: margin; left:12px; padding:0 6px; }
    QFrame#card { background:#22272e; border:1px solid #444c56; border-radius:16px; }
    QLabel#cardTitle { color:#8b949e; font-size:12px; }
    QLabel#cardValue { font-size:22px; font-weight:700; }
    """


def get_light_style() -> str:
    return """
    QWidget { background:#f6f8fa; color:#1f2328; font-size:13px; }
    QPushButton { background:white; border:1px solid #d0d7de; border-radius:8px; padding:8px 12px; }
    QPushButton:hover { background:#f3f4f6; }
    QLineEdit, QTextEdit, QComboBox, QSpinBox, QTableWidget, QListWidget { 
        background:white; border:1px solid #d0d7de; border-radius:8px; padding:6px; 
    }
    QHeaderView::section { background:#f3f4f6; padding:6px; border:none; }
    QGroupBox { border:1px solid #d0d7de; border-radius:10px; margin-top:10px; padding-top:10px; }
    QGroupBox::title { subcontrol-origin: margin; left:12px; padding:0 6px; }
    QFrame#card { background:white; border:1px solid #d0d7de; border-radius:16px; }
    QLabel#cardTitle { color:#57606a; font-size:12px; }
    QLabel#cardValue { font-size:22px; font-weight:700; }
    """


def get_style(theme: str) -> str:
    dark = """
    QWidget {
        background: #111827;
        color: #e5e7eb;
        font-size: 14px;
    }

    QMainWindow, QWidget#statusCard {
        background: #111827;
    }

    QListWidget, QTextEdit, QTableWidget, QLineEdit, QComboBox, QSpinBox {
        background: #172033;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 6px;
        color: #e5e7eb;
    }

    QPushButton, QToolButton {
        background: #1f2937;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 10px 16px;
        color: #e5e7eb;
    }

    QPushButton:hover, QToolButton:hover {
        background: #273449;
    }

    QPushButton:disabled, QToolButton:disabled {
        background: #151c2b;
        color: #7c8799;
        border: 1px solid #2a3448;
    }

    QGroupBox {
        border: 1px solid #334155;
        border-radius: 14px;
        margin-top: 10px;
        padding-top: 14px;
        font-weight: 600;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 6px;
    }

    QStatusBar {
        color: #cbd5e1;
    }

    #statusCard {
        background: #172033;
        border: 1px solid #334155;
        border-radius: 18px;
    }

    #statusCardTitle {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 600;
    }

    #statusCardValue {
        color: #e5e7eb;
        font-size: 24px;
        font-weight: 700;
    }

    QLabel[statusState="running"] {
        color: #22c55e;
    }

    QLabel[statusState="starting"], QLabel[statusState="stopping"], QLabel[statusState="restarting"] {
        color: #f59e0b;
    }

    QLabel[statusState="stopped"] {
        color: #94a3b8;
    }

    QLabel[statusState="error"] {
        color: #ef4444;
    }
    """

    light = """
    QWidget {
        background: #f8fafc;
        color: #0f172a;
        font-size: 14px;
    }

    QMainWindow, QWidget#statusCard {
        background: #f8fafc;
    }

    QListWidget, QTextEdit, QTableWidget, QLineEdit, QComboBox, QSpinBox {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 6px;
        color: #0f172a;
    }

    QPushButton, QToolButton {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 10px 16px;
        color: #0f172a;
    }

    QPushButton:hover, QToolButton:hover {
        background: #f1f5f9;
    }

    QPushButton:disabled, QToolButton:disabled {
        background: #f8fafc;
        color: #94a3b8;
        border: 1px solid #dbe3ef;
    }

    QGroupBox {
        border: 1px solid #cbd5e1;
        border-radius: 14px;
        margin-top: 10px;
        padding-top: 14px;
        font-weight: 600;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 6px;
    }

    QStatusBar {
        color: #334155;
    }

    #statusCard {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 18px;
    }

    #statusCardTitle {
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
    }

    #statusCardValue {
        color: #0f172a;
        font-size: 24px;
        font-weight: 700;
    }

    QLabel[statusState="running"] {
        color: #16a34a;
    }

    QLabel[statusState="starting"], QLabel[statusState="stopping"], QLabel[statusState="restarting"] {
        color: #d97706;
    }

    QLabel[statusState="stopped"] {
        color: #64748b;
    }

    QLabel[statusState="error"] {
        color: #dc2626;
    }
    """

    return light if theme == "light" else dark