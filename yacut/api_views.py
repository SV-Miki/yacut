"""API-эндпоинты проекта YaCut."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from yacut import app
from yacut.constants import (
    DUPLICATED_SHORT_ID_MESSAGE,
    INVALID_SHORT_ID_MESSAGE,
    RESERVED_SHORT_IDS,
    SHORT_ID_MAX_LENGTH,
)
from yacut.models import URLMap


def is_valid_short_id(short_id: str) -> bool:
    """Проверяет, что короткий идентификатор состоит из латиницы и цифр."""
    return short_id.isalnum() and short_id.isascii()


def make_error_response(message: str, status_code: HTTPStatus):
    """Формирует JSON-ответ с ошибкой."""
    response = jsonify({'message': message})
    response.status_code = status_code
    return response


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создаёт короткую ссылку через API."""
    data: dict[str, Any] | None = request.get_json(silent=True)

    if data is None:
        return make_error_response(
            'Отсутствует тело запроса',
            HTTPStatus.BAD_REQUEST,
        )

    if 'url' not in data:
        return make_error_response(
            '"url" является обязательным полем!',
            HTTPStatus.BAD_REQUEST,
        )

    custom_id = data.get('custom_id') or None

    if custom_id is not None:
        if (
            len(custom_id) > SHORT_ID_MAX_LENGTH
            or not is_valid_short_id(custom_id)
            or custom_id in RESERVED_SHORT_IDS
        ):
            return make_error_response(
                INVALID_SHORT_ID_MESSAGE,
                HTTPStatus.BAD_REQUEST,
            )

        if URLMap.get(custom_id) is not None:
            return make_error_response(
                DUPLICATED_SHORT_ID_MESSAGE,
                HTTPStatus.BAD_REQUEST,
            )

    try:
        url_map = URLMap.create(
            original=data['url'],
            short=custom_id,
        )
    except SQLAlchemyError:
        return make_error_response(
            'Ошибка при создании короткой ссылки',
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    response = jsonify(url_map.to_dict())
    response.status_code = HTTPStatus.CREATED
    return response


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_original_link(short_id: str):
    """Возвращает оригинальную ссылку по короткому идентификатору."""
    short_id = short_id.rstrip('/').split('/')[-1]

    url_map = URLMap.get(short_id)

    if url_map is None:
        return make_error_response(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND,
        )

    return jsonify({'url': url_map.original})
