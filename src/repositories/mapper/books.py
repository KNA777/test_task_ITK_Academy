from src.models.books import Book
from src.repositories.mapper.base import BaseMapper
from src.schemas.books import BooksResponse


class BooksMapper(BaseMapper):
    db_model = Book
    schema = BooksResponse