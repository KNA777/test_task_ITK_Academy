from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.config.config import settings

engine = create_async_engine(url=settings.DB_URL)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Базовый класс для всех SQLAlchemy-моделей.

       Автоматически генерирует имена таблиц на основе имени класса.
    """

    # noinspection PyMethodParameters
    @declared_attr.directive
    def __tablename__(cls):
        """Генерирует имя таблицы в lowercase на основе имени класса.

                Returns:
                    str: Имя таблицы в нижнем регистре.
        """
        return cls.__name__.lower()
