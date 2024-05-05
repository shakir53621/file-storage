from pydantic import BaseModel


class SchemaUsers(BaseModel):
    """
    Схема пользователей

    Attributes:

        user_id: id пользователя
        user_name: имя пользователя
        password: пароль пользователя
    """

    user_id: int
    user_name: str
    password: str


class SchemaUserFiles(BaseModel):
    """
    Схема файлов пользователей

    Attributes:

        file_id: id файла
        user_id: id пользователя
        file_hash: хэш названия файла
    """

    file_id: int
    user_id: int
    file_hash: str
