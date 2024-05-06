from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from app.config import files_settings
from app.file_manager.directory_manager import DirectoryManager
from app.files.routers import router as router_files
from app.auth.routers import router as router_auth


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    directory_manager = DirectoryManager()
    directory_manager.create_directory(files_settings.root_directory)

    print("Application initialized...")
    yield
    print("Application closed")


app = FastAPI(lifespan=lifespan)

app.include_router(router=router_files)
app.include_router(router=router_auth)
