import os

from fastapi import UploadFile, HTTPException, status
from starlette.responses import FileResponse

from app.db.database import async_session_maker
from app.db.models import UserFiles
from app.db.repository import BaseRepository
from app.file_manager.directory_manager import AbstractDirectoryManager
from app.file_manager.file_manager import AbstractFileManager
from app.hasher import AbstractHasher


class FileCreatorService:
    def __init__(
            self,
            hasher: AbstractHasher,
            directory_manager: AbstractDirectoryManager,
            file_manager: AbstractFileManager,
    ) -> None:
        self._hasher = hasher
        self._directory_manager = directory_manager
        self._file_manager = file_manager

    async def create_file_in_sub_directory(self, store_root: str, file: UploadFile, user_id: int) -> str:
        """
        Метод хэширует название файла, создает поддиректорию с первыми двумя символами от хеша,
        проверяет, создана ли корневая директория, копирует в эту директорию выбранный файл
        и добавляет в базу данных user_id и хэшированное название файла
        """
        file_hash = self._hasher.hash_str(string=file.filename)

        prefix = file_hash[:2]
        path_to_directory = os.path.join(store_root, prefix)

        self._directory_manager.create_directory(directory_path=path_to_directory)
        self._file_manager.create_file(path_to_directory, file, file_hash)

        async with async_session_maker() as session:
            repository = BaseRepository(session, UserFiles)
            await repository.add(user_id=user_id, file_hash=file_hash)
            await session.commit()

        return file_hash


class FileDownloaderService:
    def __init__(self, file_manager: AbstractFileManager) -> None:
        self._file_manager = file_manager

    def download_file(self, store_root: str, file_name: str):

        path_to_directory = os.path.join(store_root, file_name[:2])
        path_to_file = self._file_manager.find_path_to_file(path_to_directory, file_name)

        return FileResponse(
            path=path_to_file, filename=file_name,
            media_type='multipart/form-data'
        )


class FileDeleterService:
    def __init__(self, file_manager: AbstractFileManager) -> None:
        self._file_manager = file_manager

    async def delete_file(self, store_root: str, file_name: str, user_id: int) -> None:

        async with async_session_maker() as session:
            repository = BaseRepository(session, UserFiles)
            if await repository.find_one_or_none(user_id == UserFiles.user_id):

                path_to_directory = os.path.join(store_root, file_name[:2])
                path_to_file = self._file_manager.find_path_to_file(path_to_directory, file_name)

                await repository.delete_one_or_none(file_name == UserFiles.file_hash)
                await session.commit()

                self._file_manager.delete_file(path_to_file)
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
