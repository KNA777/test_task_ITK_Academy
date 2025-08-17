from fastapi import HTTPException

from src.constants import HTTP_404, HTTP_409, HTTP_500


class MyBaseException(Exception):
    """Базовое исключение для пользовательских исключений приложения.
    """

    detail = "Error"

    def __init__(self, *args, **kwargs):
        """Инициализирует исключение с сообщением `detail`."""
        super().__init__(self.detail)


class ObjectNotFoundException(MyBaseException):
    """Исключение: объект не найден в БД.

        Attributes:
            detail (str): Сообщение об ошибке ("Error object not found").
    """

    detail = "Error object not found"


class UniqueObjectException(MyBaseException):
    """Исключение: нарушение уникальности при создании/обновлении объекта.

        Attributes:
            detail (str): Сообщение об ошибке ("Error object create").
    """

    detail = "Error object create"


class MyBaseHTTPException(HTTPException):
    """Базовое HTTP-исключение для FastAPI.

        Attributes:
            status_code (int): HTTP-статус код по умолчанию (500).
            detail (str|dict): Детали ошибки по умолчанию ("Error").
    """

    status_code = HTTP_500
    detail = "Error"

    def __init__(self):
        """Инициализирует исключение с заданными `status_code` и `detail`.
        """
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectNotFoundHTTPException(MyBaseHTTPException):
    """HTTP-исключение: объект не найден (404).

        Attributes:
            status_code (int): HTTP-статус код (404).
            detail (dict): Детали ошибки в формате JSON:
                - status_code (int): 404
                - message (str): "Object do not exist in db"
    """

    status_code = HTTP_404
    detail = {
        "status_code": status_code,
        "message": "Object do not exist in db"
    }


class UniqueObjectHTTPException(MyBaseHTTPException):
    """HTTP-исключение: конфликт уникальности (409).

        Attributes:
            status_code (int): HTTP-статус код (409).
            detail (dict): Детали ошибки в формате JSON:
                - status_code (int): 409
                - message (str): "Book with this title already exists"
                - conflicting_field (str): Поле с конфликтом ("title")
    """

    status_code = HTTP_409
    detail = {
        "status_code": status_code,
        "message": "Book with this title already exists",
        "conflicting_field": "title"
    }
