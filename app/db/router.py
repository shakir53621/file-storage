from fastapi import APIRouter

from app.db.repositories import UsersRepository
from app.db.schemas import SchemaUsers

router = APIRouter(
    prefix="/database",
    tags=["База данных"]
)


@router.get("/all-users")
async def get_all_users() -> list[SchemaUsers]:
    """Получить всех пользователей"""
    return await UsersRepository.find_all()


@router.post("/file")
async def post_file():
    # Логика заполнения бд
    pass