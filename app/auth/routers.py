from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.models import Token
from app.auth.service import authenticate_user, create_token
from app.config import auth_settings
from app.db.models import Users

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и авторизация"],
)


@router.post("/token")
async def login_for_access_token(user: Annotated[Users, Depends(authenticate_user)]) -> Token:
    token = create_token({"user_id": user.user_id})

    return Token(access_token=token, token_type=auth_settings.token_type)
