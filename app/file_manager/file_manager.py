import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path

from fastapi import HTTPException, UploadFile, status


class AbstractFileManager(ABC):
    @abstractmethod
    def create_file(self, directory: str, file: UploadFile, file_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_path_to_file(self, directory: str, file_name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, path_to_file: str) -> None:
        raise NotImplementedError


class FileManager(AbstractFileManager):
    def create_file(self, directory: str, file: UploadFile, file_name: str) -> None:
        file_path = os.path.join(directory, file_name)
        path = Path(file_path)

        with path.open("wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

    def find_path_to_file(self, directory: str, file_name: str) -> str:
        if not os.path.exists(directory):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Директория не найдена")

        path_to_file = os.path.join(directory, file_name)

        if not os.path.exists(path_to_file):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Файл не найден")

        return path_to_file

    def delete_file(self, path_to_file: str) -> None:
        os.remove(path_to_file)
