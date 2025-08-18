from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.books import Book
from src.repositories.mapper.books import BooksMapper


class BooksRepository(BaseRepository):

    model = Book
    mapper = BooksMapper


    async def get_filtered_books_list(
            self,
            author,
            title,
            date_of_writing,
            limit,
            offset,
    ):

        query = select(self.model)

        if date_of_writing:
            years_of_writing = select(self.model.date_of_writing)
            query = query.filter(Book.date_of_writing.in_(years_of_writing))

        if author:
            query = query.filter(
                func.lower(Book.author).contains((func.lower(author)))
            )
        if title:
            query = query.filter(
                func.lower(Book.title).contains((func.lower(title)))
            )

        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return [self.mapper.map_to_schemas_object(model) for model in result.scalars().all()]
