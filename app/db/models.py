from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str]
    password: Mapped[str]


class UserFiles(Base):
    __tablename__ = 'user_files'

    file_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    file_hash: Mapped[str]
