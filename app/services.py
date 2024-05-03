import os

from fastapi import UploadFile

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
    def __init__(self) -> None:
        ...

    def download_file(self):
        ...


class FileDeleterService:
    def __init__(self) -> None:
        ...

    def delete_file(self):
        ...
