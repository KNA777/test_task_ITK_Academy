from fastapi import status
from fastapi.openapi.models import Example

HTTP_200 = status.HTTP_200_OK
HTTP_201 = status.HTTP_201_CREATED
HTTP_204 = status.HTTP_204_NO_CONTENT
HTTP_404 = status.HTTP_404_NOT_FOUND
HTTP_409 = status.HTTP_409_CONFLICT
HTTP_422 = status.HTTP_422_UNPROCESSABLE_ENTITY
HTTP_500 = status.HTTP_500_INTERNAL_SERVER_ERROR
HTTP_200_LIST = status.HTTP_200_OK

API_RESPONSE = {
    HTTP_200: {
        "description": "Successful deletion",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 200,
                    "book": {
                        "id": 1,
                        "title": "Example Book",
                        "author": "Author Name",
                        "date_of_writing": 2023
                    }
                }
            }
        }
    },
    HTTP_200_LIST: {
        "description": "Successful deletion",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 200,
                    "books": [
                        {"id": 1,
                         "title": "Example Book",
                         "author": "Author Name",
                         "date_of_writing": 1988},

                        {"id": 4,
                         "title": "Example Book",
                         "author": "Author Name",
                         "date_of_writing": 2012},

                        {"id": 7,
                         "title": "Example Book",
                         "author": "Author Name",
                         "date_of_writing": 2023},
                    ]
                }
            }
        }
    },
    HTTP_201: {
        "description": "Book successfully created",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 201,
                    "created_object": {
                        "id": 1,
                        "title": "The Great Gatsby",
                        "author": "F. Scott Fitzgerald",
                        "date_of_writing": 1925,
                    }
                }
            }
        }
    },
    HTTP_204: {
        "description": "Book successfully deleted",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 204,
                    "deleted_obj": {
                        "id": 1,
                        "title": "Example Book",
                        "author": "Author Name",
                        "date_of_writing": 2023
                    }
                }
            }
        }
    },
    HTTP_404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "status_code": 404,
                        "message": "Object do not exist in db"
                    }
                }
            }
        }

    },
    HTTP_409: {
        "description": "Conflict - Duplicate entry",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "status_code": 409,
                        "message": "Book with this title already exists",
                        "conflicting_field": "title"
                    }
                }
            }
        }
    },
    HTTP_422: {
        "description": "Validation Error - Invalid input data",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 422,
                    "detail": [
                        {
                            "loc": ["body", "title"],
                            "msg": "field required",
                            "type": "value_error.missing"
                        },
                        {
                            "loc": ["body", "author"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        }
                    ]
                }
            }
        }
    },
}

OPENAPI_EXAMPLES = openapi_examples = {
            "Example 1": Example(
                summary="Пример №1",
                value={
                    "title": "Мастер и Маргарита",
                    "author": "Михаил Булгаков",
                }
            ),
            "Example 2": Example(
                summary="Пример №2",
                value={
                    "title": "Евгений Онегин",
                    "author": "Александр Пушкин",
                    "date_of_writing": 1831
                }
            ),
            "Example 3": Example(
                summary="Пример №3",
                value={
                    "title": "Анна Каренина",
                    "author": "Лев Толстой",
                }
            )
}


API_GET_DESCRIPTION = ("<h2>Эндпоинт для получения "
                       "объекта модели book из БД по ID.</h2>")
API_GET_SUMMARY = "Получение объекта"


API_GET_ALL_DESCRIPTION = ("</h2>Эндпоинт для получения всех "
                           "объектов книги из БД.</h2>")
API_GET_ALL_SUMMARY = "Получение всех объектов"


API_POST_DESCRIPTION = ("<h2>Эндпоинт для создания "
                        "объекта книги в БД по трем полям в теле запроса: \n"
                        "- title,\n"
                        "- author,\n"
                        "- date_of_writing (необязательное поле).</h2>")
API_POST_SUMMARY = "Создание объекта"


API_PATCH_DESCRIPTION = ("<h2>Эндпоинт для частичного изменения "
                         "объекта книги в БД по ID.</h2>")
API_PATCH_SUMMARY = "Частичное редактирование объекта"


API_PUT_DESCRIPTION = ("<h2>Эндпоинт для полного изменения "
                       "объекта книги из БД по ID.</h2>")
API_PUT_SUMMARY = "Полное редактирование объекта"


API_DELETE_DESCRIPTION = ("<h2>Эндпоинт для безвозвратного "
                          "удаления объекта книги из БД по ID.</h2>")
API_DELETE_SUMMARY = "Удаление объекта"
