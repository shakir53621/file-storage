from fastapi import HTTPException, status


class FileStorageInformationException(HTTPException):
    status_code: status = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = ""

    def __init__(
            self,
            status_code: status = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail: str = ""
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class NoResultFoundInDatabaseException(FileStorageInformationException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Отсутствует запись в базе данных:\n"

    def __init__(self, table_name: str) -> None:
        super().__init__(self.status_code, self.detail + table_name)


class NoSetFilterException(FileStorageInformationException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Не задан фильтр при выборке данных для таблицы: "

    def __init__(self, table_name: str) -> None:
        super().__init__(self.status_code, self.detail + table_name)


class NoSetDataException(FileStorageInformationException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Не заданы данные при попытке добавления/обновления записи в таблице: "

    def __init__(self, table_name: str) -> None:
        super().__init__(self.status_code, self.detail + table_name)


class ModelIsNotSetException(FileStorageInformationException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Отсутствует связь репозитория и модели БД"

    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail)


class MissingKeyError(FileStorageInformationException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Отсутствует ключ в словаре"

    def __init__(self, detail: str | None = None) -> None:
        if detail:
            self.detail = detail
        super().__init__(self.status_code, self.detail)
