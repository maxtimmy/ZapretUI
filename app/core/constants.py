STATUS_STOPPED = 'stopped'
STATUS_STARTING = 'starting'
STATUS_RUNNING = 'running'
STATUS_ERROR = 'error'

PAGE_DASHBOARD = 'дашборд'
PAGE_PROFILES = 'профили'
PAGE_LOGS = 'логи'
PAGE_SETTINGS = 'настройки'

DEFAULT_PROFILE = {
    'name': 'default',
    'interface': '',
    'dns': '1.1.1.1',
    'mode': 'normal',
    'timeout': 30,
    'autostart': False,
    'command': '',
    'domains': ['example.com'],
}

DEFAULT_SETTINGS = {
    'default_profile': 'default',
    'theme': 'dark',
    'to_tray': True,
    'auto_save': True,
    'window_width': 1280,
    'window_height': 820,
}
