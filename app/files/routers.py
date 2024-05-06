from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from fastapi.responses import FileResponse

from app.auth.service import get_user_by_jwt_token
from app.config import files_settings
from app.db.models import Users
from app.file_manager.directory_manager import AbstractDirectoryManager, DirectoryManager
from app.file_manager.file_manager import AbstractFileManager, FileManager
from app.hasher import AbstractHasher, MD5Hasher
from app.files.services import FileCreatorService, FileDownloaderService, FileDeleterService

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
        current_user: Annotated[Users, Depends(get_user_by_jwt_token)]
):
    file_service = FileCreatorService(
        hasher=hasher,
        directory_manager=directory_manager,
        file_manager=file_manager,
    )

    if current_user:
        return await file_service.create_file_in_sub_directory(
            store_root=files_settings.root_directory,
            file=file,
            user_id=current_user.user_id
        )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/download-file")
async def download_file(
        file_name: str,
        file_manager: Annotated[AbstractFileManager, Depends(FileManager)],
) -> FileResponse:
    file_service = FileDownloaderService(file_manager)

    return file_service.download_file(store_root=files_settings.root_directory, file_name=file_name)


@router.delete("/delete-file")
async def delete_file(
        file_name: str,
        file_manager: Annotated[AbstractFileManager, Depends(FileManager)],
        current_user: Annotated[Users, Depends(get_user_by_jwt_token)]
):
    file_service = FileDeleterService(file_manager)

    return await file_service.delete_file(
        store_root=files_settings.root_directory,
        file_name=file_name,
        user_id=current_user.user_id
    )
