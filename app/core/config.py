from pathlib import Path

APP_NAME = 'net control'
APP_VERSION = '0.1.0'
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / 'data'
CONFIG_PATH = DATA_DIR / 'settings.json'
LOG_PATH = DATA_DIR / 'app.log'

DATA_DIR.mkdir(parents=True, exist_ok=True)
