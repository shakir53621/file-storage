from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

async_engine = create_async_engine(
    settings.database_url,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    poolclass=NullPool
)
async_session_maker = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
