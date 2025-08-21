from fastapi import APIRouter, Path, Body, Query

from src.constants import (API_RESPONSE, HTTP_200, HTTP_201,
                           HTTP_404, HTTP_409, HTTP_422,
                           HTTP_204, API_PUT_DESCRIPTION,
                           API_PUT_SUMMARY, API_GET_SUMMARY,
                           API_GET_DESCRIPTION, API_PATCH_SUMMARY,
                           API_POST_SUMMARY, API_POST_DESCRIPTION,
                           API_PATCH_DESCRIPTION, API_DELETE_SUMMARY,
                           OPENAPI_EXAMPLES, API_DELETE_DESCRIPTION,
                           API_GET_ALL_DESCRIPTION, API_GET_ALL_SUMMARY,
                           HTTP_200_LIST, CURRENT_YEAR)
from src.dependencies.dependencies import DBDep
from src.exceptions.exceptions import (ObjectNotFoundException,
                                       ObjectNotFoundHTTPException,
                                       UniqueObjectException,
                                       UniqueObjectHTTPException)
from src.schemas.books import (BooksResponse, BooksRequestAdd,
                               BooksRequestPUT, BooksRequestPATCH)

router = APIRouter(prefix="/books", tags=["Книги"])


@router.get(path="/{book_id}",
            responses={
                HTTP_200: API_RESPONSE[HTTP_200],
                HTTP_404: API_RESPONSE[HTTP_404],
            },
            summary=API_GET_SUMMARY,
            description=API_GET_DESCRIPTION)
async def get_book(
        db: DBDep,
        book_id: int = Path(description="ID объекта", example="1")
) -> dict[str, str | int | BooksResponse]:
    try:
        book = await db.books.get_one_by_id(id=book_id)
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException()
    return {
        "status": HTTP_200,
        "book": book
    }


@router.get(path="",
            responses={
                HTTP_200_LIST: API_RESPONSE[HTTP_200_LIST]
            },
            summary=API_GET_ALL_SUMMARY,
            description=API_GET_ALL_DESCRIPTION)
async def get_list_filtered_books(
        db: DBDep,
        author: str | None = Query(None, description="Имя/Фамилия автора"),
        title: str | None = Query(None, description="Название книги"),
        date_of_writing: int | None = Query(
            None, le=CURRENT_YEAR ,description="Год написания"),
        page: int | None = Query(1, gt=0, description="Номер страницы"),
        per_page: int | None = Query(3, description="Количество книг на странице")
) -> dict[str, str | int | list[BooksResponse | None]]:
    books = await db.books.get_filtered_books_list(
        author=author,
        title=title,
        date_of_writing=date_of_writing,
        limit=per_page,
        offset=per_page * (page - 1)
    )
    return {
        "status_code": HTTP_200,
        "books": books
    }


@router.post(path="",
             responses={
                 HTTP_200: API_RESPONSE[HTTP_200],
                 HTTP_201: API_RESPONSE[HTTP_201],
                 HTTP_409: API_RESPONSE[HTTP_409],
             },
             summary=API_POST_SUMMARY,
             description=API_POST_DESCRIPTION)
async def create_book(
        db: DBDep,
        book_data: BooksRequestAdd = Body(
            openapi_examples=OPENAPI_EXAMPLES)
) -> dict[str, str | int | BooksResponse]:
    try:
        book = await db.books.create(book_data)
    except UniqueObjectException:
        raise UniqueObjectHTTPException()
    return {
        "status": HTTP_201,
        "book": book
    }


@router.patch(path="/{book_id}",
              responses={
                  HTTP_200: API_RESPONSE[HTTP_200],
                  HTTP_404: API_RESPONSE[HTTP_404],
                  HTTP_409: API_RESPONSE[HTTP_409],
                  HTTP_422: API_RESPONSE[HTTP_422],
              },
              summary=API_PATCH_SUMMARY,
              description=API_PATCH_DESCRIPTION)
async def partitial_edit_book(
        db: DBDep,
        book_id: int,
        book_data: BooksRequestPATCH

) -> dict[str, str | int | BooksResponse]:
    try:
        book = await db.books.edit(book_data, id=book_id, exclude_unset=True)
    except UniqueObjectException:
        raise UniqueObjectHTTPException()
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException()
    return {
        "status_code": HTTP_200,
        "book": book
    }


@router.put(path="/{book_id}",
            responses={
                HTTP_200: API_RESPONSE[HTTP_200],
                HTTP_404: API_RESPONSE[HTTP_404],
                HTTP_409: API_RESPONSE[HTTP_409],
                HTTP_422: API_RESPONSE[HTTP_422],
            },
            summary=API_PUT_SUMMARY,
            description=API_PUT_DESCRIPTION)
async def full_edit_book(
        db: DBDep,
        book_data: BooksRequestPUT,
        book_id: int = Path(description="ID объекта", example="1")
) -> dict[str, str | int | BooksResponse]:
    try:
        book = await db.books.edit(book_data, id=book_id)
    except UniqueObjectException:
        raise UniqueObjectHTTPException()
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException()
    return {
        "status_code": HTTP_200,
        "deleted_obj": book
    }


@router.delete(
    path="/{book_id}",
    responses={
        HTTP_204: API_RESPONSE[HTTP_204]},
    summary=API_DELETE_SUMMARY,
    description=API_DELETE_DESCRIPTION
)
async def delete_book(
        db: DBDep,
        book_id: int = Path(description="ID объекта", example="1")
) -> dict[str, str | int | BooksResponse]:
    try:
        deleted_obj = await db.books.delete(id=book_id)
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException()
    return {
        "status": HTTP_204,
        "deleted_obj": deleted_obj
    }
