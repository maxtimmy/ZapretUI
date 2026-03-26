from pathlib import Path

APP_NAME = "Net Control"
APP_VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
LOG_DIR = DATA_DIR / "logs"
CONFIG_FILE = DATA_DIR / "settings.json"
LOG_FILE = LOG_DIR / "app.log"

DEFAULT_THEME = "dark"

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
