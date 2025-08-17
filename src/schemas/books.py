from pydantic import BaseModel


class Books(BaseModel):
    id: int


class BooksResponse(Books):
    title: str
    author: str
    date_of_writing: int | None = None


class BooksRequestAdd(BaseModel):
    title: str
    author: str
    date_of_writing: int | None = None


class BooksRequestPUT(BaseModel):
    title: str
    author: str
    date_of_writing: int


class BooksRequestPATCH(BaseModel):
    title: str | None = None
    author: str | None = None
    date_of_writing: int | None = None
