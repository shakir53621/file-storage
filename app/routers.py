import os.path
from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import FileResponse

from app.constants import STORE_ROOT
from app.file_manager.directory_manager import AbstractDirectoryManager, DirectoryManager
from app.file_manager.file_manager import AbstractFileManager, FileManager
from app.file_manager.hasher import AbstractHasher, MD5Hasher
from app.services import FileCreatorService

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

    directory_path = os.path.join(STORE_ROOT, file_name[:2])
    path_to_file = file_manager.find_path_to_file(directory=directory_path, file_name=file_name)

    return FileResponse(
        path=path_to_file, filename=file_name,
        media_type='multipart/form-data'
    )


@router.get("/delete-file")
async def delete_file(
        file_name: str,
        file_manager: Annotated[AbstractFileManager, Depends(FileManager)],
):

    directory_path = os.path.join(STORE_ROOT, file_name[:2])
    try:
        if directory_path:
            path_to_file = file_manager.find_path_to_file(directory=directory_path, file_name=file_name)
            os.remove(path_to_file)
            return {"message": f"Файл {path_to_file} успешно удален"}
    except FileNotFoundError:
        return {"message": "Файл не найден"}
