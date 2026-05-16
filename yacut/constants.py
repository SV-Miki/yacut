"""Константы проекта YaCut."""

from __future__ import annotations

from string import ascii_letters, digits

SHORT_ID_DEFAULT_LENGTH = 6
SHORT_ID_MAX_LENGTH = 16
SHORT_ID_CHARS = ascii_letters + digits
SHORT_ID_GENERATION_ATTEMPTS = 100
SHORT_ID_PATTERN = r'^[A-Za-z0-9]*$'

RESERVED_SHORT_IDS = {'files'}

DUPLICATED_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
INVALID_SHORT_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'

BASE_URL = 'http://localhost'

YANDEX_DISK_API_URL = 'https://cloud-api.yandex.net/v1/disk'
YANDEX_DISK_UPLOAD_URL = f'{YANDEX_DISK_API_URL}/resources/upload'
YANDEX_DISK_DOWNLOAD_URL = f'{YANDEX_DISK_API_URL}/resources/download'
YANDEX_DISK_UPLOAD_FOLDER = 'yacut'
