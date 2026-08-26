"""Асинхронная работа с API Яндекс Диска."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

import aiohttp
from flask import current_app
from werkzeug.datastructures import FileStorage

from yacut.constants import (
    YANDEX_DISK_DOWNLOAD_URL,
    YANDEX_DISK_UPLOAD_FOLDER,
    YANDEX_DISK_UPLOAD_URL,
)


@dataclass(frozen=True)
class UploadedFile:
    """Результат загрузки одного файла."""

    name: str
    download_url: str


def get_headers() -> dict[str, str]:
    """Возвращает заголовки для запросов к API Яндекс Диска."""
    return {
        'Authorization': f'OAuth {current_app.config["DISK_TOKEN"]}',
    }


def build_disk_path(filename: str) -> str:
    """Формирует путь файла на Яндекс Диске."""
    return f'/{YANDEX_DISK_UPLOAD_FOLDER}/{filename}'


async def get_upload_link(
    session: aiohttp.ClientSession,
    disk_path: str,
) -> str:
    """Получает ссылку для загрузки файла."""
    async with session.get(
        YANDEX_DISK_UPLOAD_URL,
        headers=get_headers(),
        params={
            'path': disk_path,
            'overwrite': 'true',
            'fields': 'href',
        },
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data['href']


async def upload_file(
    session: aiohttp.ClientSession,
    upload_url: str,
    file_data: bytes,
) -> None:
    """Загружает файл по полученной ссылке."""
    async with session.put(upload_url, data=file_data) as response:
        response.raise_for_status()


async def get_download_link(
    session: aiohttp.ClientSession,
    disk_path: str,
) -> str:
    """Получает ссылку для скачивания файла."""
    async with session.get(
        YANDEX_DISK_DOWNLOAD_URL,
        headers=get_headers(),
        params={
            'path': disk_path,
            'fields': 'href',
        },
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data['href']


async def upload_one_file(
    session: aiohttp.ClientSession,
    file: FileStorage,
) -> UploadedFile:
    """Загружает один файл и возвращает ссылку для скачивания."""
    filename = file.filename or 'file'
    disk_path = build_disk_path(filename)
    file_data = file.read()

    upload_url = await get_upload_link(session, disk_path)
    await upload_file(session, upload_url, file_data)
    download_url = await get_download_link(session, disk_path)

    return UploadedFile(name=filename, download_url=download_url)


async def upload_files_to_yandex_disk(
    files: list[FileStorage],
) -> list[UploadedFile]:
    """Асинхронно загружает список файлов на Яндекс Диск."""
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *(upload_one_file(session, file) for file in files)
        )
