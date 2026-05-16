# YaCut

## Описание проекта

YaCut - сервис для сокращения длинных ссылок.

Проект позволяет:
- создавать короткие ссылки для длинных URL
- использовать пользовательские короткие идентификаторы
- автоматически генерировать уникальные короткие ссылки
- загружать несколько файлов на Яндекс Диск
- получать короткие ссылки для скачивания файлов
- выполнять переадресацию по коротким ссылкам
- работать с API для создания и получения ссылок

Также проект поддерживает асинхронную загрузку файлов на Яндекс Диск с использованием `aiohttp`.


## Технологии

В проекте используются:

- Python 3.12
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Migrate
- SQLAlchemy
- SQLite
- Alembic
- aiohttp
- Jinja2
- Bootstrap 5
- Pytest
- Flake8


## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone <URL_репозитория>
```

```bash
cd async-yacut
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv venv
```

#### Linux/macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
source venv/Scripts/activate
```

---

### 3. Установить зависимости

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

### 4. Создать файл `.env`

В корневой директории проекта создайте файл `.env`:

```env
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_token
```

## Переменные окружения

| Переменная | Описание |
|---|---|
| FLASK_APP | Flask-приложение |
| FLASK_ENV | Режим запуска Flask |
| SECRET_KEY | Секретный ключ Flask |
| DATABASE_URI | Подключение к базе данных |
| DISK_TOKEN | OAuth-токен Яндекс Диска |

### 5. Применить миграции

```bash
flask db upgrade
```

### 6. Запустить проект

```bash
flask run
```

После запуска проект будет доступен по адресу:

```text
http://127.0.0.1:5000
```

## API

Проект поддерживает API:

### Создание короткой ссылки

`POST /api/id/`

### Получение оригинальной ссылки

`GET /api/id/<short_id>/`

Документация API описана в файле `openapi.yml`.

## Автор

Владислав Шилов
