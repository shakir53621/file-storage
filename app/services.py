import os

from fastapi import UploadFile
from starlette.responses import FileResponse

from app.file_manager.directory_manager import AbstractDirectoryManager
from app.file_manager.file_manager import AbstractFileManager
from app.file_manager.hasher import AbstractHasher


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

    def create_file_in_sub_directory(self, store_root: str, file: UploadFile):
        file_hash = self._hasher.hash_str(string=file.filename)

        prefix = file_hash[:2]
        path_to_directory = os.path.join(store_root, prefix)

        self._directory_manager.create_directory(directory_path=path_to_directory)
        self._file_manager.create_file(path_to_directory, file, file_hash)

        return file_hash


class FileDownloaderService:
    def __init__(self,
                 file_manager: AbstractFileManager) -> None:
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

    def delete_file(self, store_root: str, file_name: str) -> None:

        path_to_directory = os.path.join(store_root, file_name[:2])
        path_to_file = self._file_manager.find_path_to_file(path_to_directory, file_name)

        self._file_manager.delete_file(path_to_file)
