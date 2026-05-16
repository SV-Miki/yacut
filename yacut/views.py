"""View-функции пользовательского интерфейса YaCut."""

from __future__ import annotations

import asyncio

from flask import flash, redirect, render_template
from sqlalchemy.exc import SQLAlchemyError

from yacut import app
from yacut.constants import DUPLICATED_SHORT_ID_MESSAGE, RESERVED_SHORT_IDS
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap
from yacut.yandex_disk import upload_files_to_yandex_disk


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница с формой создания короткой ссылки."""
    form = URLMapForm()
    short_link = None

    if form.validate_on_submit():
        custom_id = form.custom_id.data or None

        if (
            custom_id in RESERVED_SHORT_IDS
            or URLMap.get(custom_id) is not None
        ):
            flash(DUPLICATED_SHORT_ID_MESSAGE)
            return render_template(
                'index.html', form=form, short_link=short_link
            )

        try:
            url_map = URLMap.create(
                original=form.original_link.data,
                short=custom_id,
            )
        except SQLAlchemyError:
            flash('Ошибка при создании короткой ссылки.')
            return render_template(
                'index.html', form=form, short_link=short_link
            )

        short_link = url_map.get_short_url()

    return render_template('index.html', form=form, short_link=short_link)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    """Страница загрузки файлов на Яндекс Диск."""
    form = FileUploadForm()
    uploaded_files = []

    if form.validate_on_submit():
        files = [file for file in form.files.data if file.filename]
        disk_files = asyncio.run(upload_files_to_yandex_disk(files))

        for disk_file in disk_files:
            try:
                url_map = URLMap.create(original=disk_file.download_url)
            except SQLAlchemyError:
                flash(
                    f'Не удалось создать короткую ссылку '
                    f'для файла {disk_file.name}.'
                )
                continue

            uploaded_files.append({
                'name': disk_file.name,
                'short_link': url_map.get_short_url(),
            })

    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files,
    )


@app.route('/<string:short_id>')
def redirect_view(short_id: str):
    """Перенаправляет пользователя по короткой ссылке."""
    url_map = URLMap.get(short_id)

    if url_map is None:
        return render_template('404.html'), 404

    return redirect(url_map.original)
