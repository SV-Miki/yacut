"""Модели базы данных проекта YaCut."""

from __future__ import annotations

from datetime import datetime

from yacut import db
from yacut.constants import SHORT_ID_MAX_LENGTH


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
