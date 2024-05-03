import os
from abc import ABC, abstractmethod


class AbstractDirectoryManager(ABC):
    @abstractmethod
    def create_directory(self, directory_path: str) -> None:
        raise NotImplementedError


class DirectoryManager(AbstractDirectoryManager):
    def create_directory(self, directory_path: str) -> None:
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
