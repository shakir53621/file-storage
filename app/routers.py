from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import FileResponse

from app.constants import STORE_ROOT
from app.file_manager.directory_manager import AbstractDirectoryManager, DirectoryManager
from app.file_manager.file_manager import AbstractFileManager, FileManager
from app.file_manager.hasher import AbstractHasher, MD5Hasher
from app.services import FileCreatorService, FileDownloaderService, FileDeleterService

router = APIRouter(
    prefix="/files",
    tags=["Работа с файлами"],
)


@router.post("/upload-file")
async def upload_file(
        file: UploadFile,
        hasher: Annotated[AbstractHasher, Depends(MD5Hasher)],
        directory_manager: Annotated[AbstractDirectoryManager, Depends(DirectoryManager)],
        file_manager: Annotated[AbstractFileManager, Depends(FileManager)],
):
    file_service = FileCreatorService(
        hasher=hasher,
        directory_manager=directory_manager,
        file_manager=file_manager,
    )

    return file_service.create_file_in_sub_directory(
        store_root=STORE_ROOT,
        file=file,
    )


@router.get("/download-file")
async def download_file(
        file_name: str,
        file_manager: Annotated[AbstractFileManager, Depends(FileManager)],
) -> FileResponse:

    file_service = FileDownloaderService(file_manager)

    return file_service.download_file(store_root=STORE_ROOT, file_name=file_name)


@router.delete("/delete-file")
async def delete_file(
        file_name: str,
        file_manager: Annotated[AbstractFileManager, Depends(FileManager)],
):
    file_service = FileDeleterService(file_manager)

    return file_service.delete_file(store_root=STORE_ROOT, file_name=file_name)


"""
todo:
    1. Добавить ручку удаления файла
    2. Отрефакторить ручку download_file (вынести логику в сервис)
    3. Авторизация на основе БД (поднять базу в докере, настроить .env файл)
    4. Отдавать JWT токен после авторизации
    5. Поднять в докере
"""

"""
table users:
    1. user_id
    2. user_name
    3. password (hashed)

table files:
    1. file_id
    2. user_id
    3. file_hash
"""

# 1 | 13 | 4a47a0db6e60853dedfcfdf08a5ca249
