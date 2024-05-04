from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.constants import STORE_ROOT
from app.file_manager.directory_manager import DirectoryManager
from app.routers import router
from app.db.router import router as router_db


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    directory_manager = DirectoryManager()
    directory_manager.create_directory(STORE_ROOT)

    print("Application initialized...")
    yield
    print("Application closed")


app = FastAPI(lifespan=lifespan)

app.include_router(router=router)
app.include_router(router=router_db)
