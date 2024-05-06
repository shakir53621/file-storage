import datetime
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from app.config import auth_settings
from app.db.database import async_session_maker
from app.db.models import Users
from app.db.repository import BaseRepository
from app.hasher import AbstractHasher, SHA256Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_user_by_username(username: str) -> Users | None:
    async with async_session_maker() as session:
        repository = BaseRepository(session, Users)
        user: Users | None = await repository.find_one_or_none(Users.user_name == username)

        return user


async def get_user_by_user_id(user_id: int) -> Users | None:
    """Возвращает запись пользователя из БД по user_id"""
    async with async_session_maker() as session:
        repository = BaseRepository(session, Users)
        user: Users | None = await repository.find_one_or_none(Users.user_id == user_id)

        return user


async def authenticate_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        hasher: Annotated[AbstractHasher, Depends(SHA256Hasher)],
) -> Users:
    user = await get_user_by_username(form_data.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    hasher = hasher.hash_str(form_data.password)
    if user.password == hasher:
        return user

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def create_token(payload: dict[str, Any]) -> str:
    to_encode = payload.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, auth_settings.secret_key, auth_settings.algorithm)

    return encoded_jwt


async def get_user_by_jwt_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Users | None:
    """Функция получает пользователя по jwt токену"""
    try:
        payload = jwt.decode(token, auth_settings.secret_key, algorithms=[auth_settings.algorithm])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await get_user_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user
