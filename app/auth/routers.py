from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.models import Token
from app.auth.service import authenticate_user, create_token, get_user_by_jwt_token
from app.db.models import Users
from app.schemas import SchemaUsers

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и авторизация"]
)


@router.post("/token")
async def login_for_access_token(user: Annotated[Users, Depends(authenticate_user)]) -> Token:
    token = create_token({"user_id": user.user_id})

    return Token(access_token=token, token_type="bearer")


@router.get("/users/me/")
async def read_users_me(current_user: Annotated[Users, Depends(get_user_by_jwt_token)]) -> SchemaUsers:
    """"""
    return SchemaUsers(user_id=current_user.user_id, user_name=current_user.user_name)



