from typing import Any

from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker
from app.exceptions import ModelIsNotSetException, NoSetDataException, NoSetFilterException


class BaseRepository:
    model: Any | None = None
    table_name: str = ""

    @classmethod
    async def add(cls, **data) -> model:
        """Добавить одну запись в БД"""

        if cls.model is None:
            raise ModelIsNotSetException

        if data is None or len(data) == 0:
            raise NoSetDataException(cls.table_name)

        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.__table__.columns)
            result = await session.execute(query)
            return result

    @classmethod
    async def find_one_or_none(cls, *filter_by: Any) -> Any:
        """Прочитать одну запись по фильтру"""

        if cls.model is None:
            raise ModelIsNotSetException

        if len(filter_by) < 1:
            raise NoSetFilterException(cls.table_name)

        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(*filter_by)
            result = await session.execute(query)

            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, *filter_by: Any) -> list[model]:
        """Прочитать все записи из таблицы (опционально используется фильтр)"""

        if cls.model is None:
            raise ModelIsNotSetException

        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(*filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def update(cls, *filter_by, **data) -> None:
        """Обновить запись в БД"""

        if cls.model is None:
            raise ModelIsNotSetException

        if len(filter_by) < 1:
            raise NoSetFilterException(cls.table_name)

        if data is None or len(data) == 0:
            raise NoSetDataException(cls.table_name)

        async with async_session_maker() as session:
            query = update(cls.model).filter(*filter_by).values(**data).returning(cls.model.__table__.columns)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().all()

    @classmethod
    async def delete(cls, *filter_by) -> None:
        """Удалить запись из БД"""

        if cls.model is None:
            raise ModelIsNotSetException

        if len(filter_by) < 1:
            raise NoSetFilterException(cls.table_name)

        async with async_session_maker() as session:
            query = delete(cls.model).filter(*filter_by)
            await session.execute(query)
            await session.commit()
