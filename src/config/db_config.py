from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.config.config import settings

engine = create_async_engine(url=settings.DB_URL)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):

    # noinspection PyMethodParameters
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()
