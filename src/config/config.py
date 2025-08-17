from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения с загрузкой переменных окружения.

        Содержит настройки подключения к PostgreSQL и генерирует URL для SQLAlchemy.
        Переменные загружаются из .env файла или окружения.

        Attributes:
            DB_USER: Имя пользователя БД.
            DB_PASS: Пароль пользователя БД.
            DB_HOST: Хост БД.
            DB_PORT: Порт БД.
            DB_NAME: Имя базы данных.
    """
    DB_USER: str | None = None
    DB_PASS: str | None = None
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_NAME: str | None = None

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def DB_URL(self) -> str:
        """Генерирует асинхронный URL для подключения к PostgreSQL.

                Returns:
                    str: DSN строка в формате postgresql+asyncpg://user:pass@host:port/db_name
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
