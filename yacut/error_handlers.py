"""Обработчики ошибок проекта YaCut."""

from __future__ import annotations

from http import HTTPStatus

from flask import render_template

from yacut import app


@app.errorhandler(404)
def page_not_found(error):
    """Возвращает пользовательскую страницу ошибки 404."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND
