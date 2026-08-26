"""Модели базы данных проекта YaCut."""

from __future__ import annotations

from datetime import datetime
from random import choice

from flask import url_for
from sqlalchemy.exc import SQLAlchemyError

from yacut import db
from yacut.constants import (
    SHORT_ID_CHARS,
    SHORT_ID_DEFAULT_LENGTH,
    SHORT_ID_GENERATION_ATTEMPTS,
    SHORT_ID_MAX_LENGTH,
)


class URLMap(db.Model):
    """Модель коротких ссылок."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(SHORT_ID_MAX_LENGTH),
        unique=True,
        nullable=False,
        index=True,
    )
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    @classmethod
    def get(cls, short_id: str) -> URLMap | None:
        """Возвращает объект ссылки по короткому идентификатору."""
        return cls.query.filter_by(short=short_id).first()

    @classmethod
    def get_unique_short_id(cls) -> str:
        """Генерирует уникальный короткий идентификатор."""
        for _ in range(SHORT_ID_GENERATION_ATTEMPTS):
            short_id = ''.join(
                choice(SHORT_ID_CHARS)
                for _ in range(SHORT_ID_DEFAULT_LENGTH)
            )

            if cls.get(short_id) is None:
                return short_id

        raise RuntimeError('Не удалось сгенерировать уникальный short_id')

    @classmethod
    def create(cls, original: str, short: str | None = None) -> URLMap:
        """Создаёт и сохраняет объект короткой ссылки."""
        url_map = cls(
            original=original,
            short=short or cls.get_unique_short_id(),
        )

        try:
            db.session.add(url_map)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

        return url_map

    def get_short_url(self) -> str:
        """Возвращает абсолютную короткую ссылку."""
        return url_for(
            'redirect_view',
            short_id=self.short,
            _external=True,
        )

    def to_dict(self) -> dict[str, str]:
        """Преобразует объект ссылки в словарь."""
        return {
            'url': self.original,
            'short_link': self.get_short_url(),
        }
