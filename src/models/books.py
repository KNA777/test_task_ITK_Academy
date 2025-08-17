from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.config.db_config import Base


class Book(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), unique=True)
    author: Mapped[str] = mapped_column(String(32))
    date_of_writing: Mapped[int] = mapped_column(nullable=True)


