# net_control_scaffold

Безопасный каркас десктоп-приложения на PySide6.

## Что внутри
- OOP-структура
- страницы: dashboard / profiles / logs / settings
- хранение профилей и настроек в json
- сервис логов
- безопасный запуск произвольной команды как подпроцесса
- тёмная и светлая тема
- системный трей

## Запуск
```bash
pip install -r requirements.txt
python main.py
```

## Где что лежит
- `app/models` — модели данных
- `app/services` — бизнес-логика
- `app/storage` — работа с json
- `app/controllers` — связка между ui и сервисами
- `app/ui` — окна, страницы, виджеты
