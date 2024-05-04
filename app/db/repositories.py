from app.db.models import Users, UserFiles
from app.repository import BaseRepository


class UsersRepository(BaseRepository):
    model = Users
    table_name = "Пользователи"


class UserFilesRepository(BaseRepository):
    model = UserFiles
    table_name = "Файлы пользователей"
