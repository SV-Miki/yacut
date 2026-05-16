"""Формы проекта YaCut."""

from __future__ import annotations

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import MultipleFileField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from yacut.constants import SHORT_ID_MAX_LENGTH, SHORT_ID_PATTERN


class URLMapForm(FlaskForm):
    """Форма создания короткой ссылки."""

    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Введите корректную ссылку'),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=SHORT_ID_MAX_LENGTH),
            Regexp(SHORT_ID_PATTERN),
        ],
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    """Форма загрузки нескольких файлов."""

    files = MultipleFileField(
        'Выберите файлы',
        validators=[FileRequired(message='Выберите хотя бы один файл')],
    )
    submit = SubmitField('Загрузить')
