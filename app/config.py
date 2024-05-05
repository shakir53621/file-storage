from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    DMS: str
    DMS_DRIVER: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def database_url(self) -> PostgresDsn:
        driver = f"{self.DMS}+{self.DMS_DRIVER}"
        user = f"{self.DB_USER}:{self.DB_PASSWORD}"
        database = f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"{driver}://{user}@{database}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class FilesSettings(BaseSettings):
    root_directory: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


database_settings = DatabaseSettings()
files_settings = FilesSettings()

