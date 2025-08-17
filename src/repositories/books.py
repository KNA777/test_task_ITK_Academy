from src.repositories.base import BaseRepository
from src.models.books import Book
from src.repositories.mapper.books import BooksMapper


class BooksRepository(BaseRepository):

    model = Book
    mapper = BooksMapper
