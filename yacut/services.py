"""Сервисные функции проекта YaCut."""

from __future__ import annotations

from random import choice

from yacut import db
from yacut.constants import SHORT_ID_CHARS, SHORT_ID_DEFAULT_LENGTH
from yacut.models import URLMap


def get_unique_short_id() -> str:
    """Генерирует уникальный короткий идентификатор."""
    while True:
        short_id = ''.join(
            choice(SHORT_ID_CHARS) for _ in range(SHORT_ID_DEFAULT_LENGTH)
        )
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id


def create_url_map(original: str, short: str | None = None) -> URLMap:
    """Создаёт объект короткой ссылки и сохраняет его в базе."""
    url_map = URLMap(
        original=original,
        short=short or get_unique_short_id(),
    )
    db.session.add(url_map)
    db.session.commit()
    return url_map
