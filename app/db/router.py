from typing import Annotated

from fastapi import APIRouter, Query

from app.db.repositories import UsersRepository
from app.db.schemas import SchemaUsers
from app.db.models import Users

router = APIRouter(
    prefix="/database",
    tags=["База данных"]
)


@router.get("/all-users")
async def get_all_users() -> list[SchemaUsers]:
    """Получить всех пользователей"""
    return await UsersRepository.find_all()


@router.get("/user")
async def get_user_id(user_id: Annotated[int, Query(ge=1, description="id пользователя")]) -> SchemaUsers | None:
    """Получить пользователя по id"""
    return await UsersRepository.find_one_or_none(Users.user_id == user_id)


@router.post("/file_user")
async def post_file():
    # Логика заполнения бд
    pass
