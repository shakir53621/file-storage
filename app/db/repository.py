from typing import Any

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import Base


class BaseRepository:
    def __init__(self, session: AsyncSession, model: type[Base]) -> None:
        self._session = session
        self._model = model

    async def add(self, autocommit: bool = False, **data) -> Any:
        """Добавить одну запись в БД"""

        query = insert(self._model).values(**data).returning(self._model.__table__.columns)
        result = await self._session.execute(query)
        if autocommit:
            await self._session.commit()
        return result

    async def find_one_or_none(self, *filter_by: Any) -> Any:
        """Прочитать одну запись по фильтру"""

        query = select(self._model.__table__.columns).filter(*filter_by)
        result = await self._session.execute(query)

        return result.mappings().one_or_none()

    async def delete_all(self, autocommit: bool = False, *filter_by: Any) -> None:
        """Удалить запись из БД"""

        query = delete(self._model).filter(*filter_by)
        await self._session.execute(query)
        if autocommit:
            await self._session.commit()

    async def delete_one_or_none(self, *filter_by: Any) -> None:
        """Удалить одну запись из БД по фильтру, если она существует"""

        query = select(self._model).filter(*filter_by)
        result = await self._session.execute(query)
        instance = result.scalars().one_or_none()

        if instance:
            delete_query = delete(self._model).where(*filter_by)
            await self._session.execute(delete_query)
            await self._session.commit()
