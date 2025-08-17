from typing import Annotated

from fastapi import Depends

from src.config.db_config import async_session
from src.config.db_context_manager import DBManager


async def get_db():
    """Асинхронный генератор для внедрения зависимостей (Dependency Injection) сессии БД.

        Используется как зависимость в FastAPI для предоставления сессии базы данных
        в обработчики маршрутов. Гарантирует корректное управление жизненным циклом сессии.

        Yields:
            DBManager: Менеджер сессии БД с инициализированными репозиториями.

        Пример использования в FastAPI:
            ```python
            @router.get("/items")
            async def read_items(db: DBManager = Depends(get_db)):
                items = await db.items.get_all()
                return items
            ```

        Примечания:
            - Автоматически закрывает сессию после завершения работы обработчика
            - Не требует ручного вызова commit()/rollback() - это делается в __aexit__ DBManager
    """
    async with DBManager(session_factory=async_session) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
