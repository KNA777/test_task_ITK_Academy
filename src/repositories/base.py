from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from pydantic import BaseModel

from src.exceptions.exceptions import ObjectNotFoundException, UniqueObjectException


class BaseRepository:
    """Базовый репозиторий для работы с моделями SQLAlchemy.

        Предоставляет CRUD-операции (create, read, update, delete) для моделей БД.
        Использует асинхронный SQLAlchemy и автоматическое маппирование в Pydantic-схемы.
    """

    model = None
    mapper = None

    def __init__(self, session):
        """Инициализирует репозиторий с сессией SQLAlchemy."""
        self.session = session

    async def get_all(self):
        """Получает все записи из таблицы."""
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_by_id(self, **filter_by):
        """Получает одну запись по ID или другим фильтрам.

        Args:
            **filter_by: Параметры фильтрации (например, `id=1`).

        Returns:
            BaseModel: Объект, преобразованный в Pydantic-схему.

        Raises:
            ObjectNotFoundException: Если объект не найден.
        """
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_schemas_object(model)

    async def create(self, data: BaseModel):
        """Создает новую запись в БД.

        Args:
            data (BaseModel): Pydantic-схема с данными для создания.

        Raises:
            UniqueObjectException: Если нарушено ограничение уникальности.
        """
        stmt = (insert(self.model)
                .values(**data.model_dump(exclude_unset=True))
                .returning(self.model))
        try:
            result = await self.session.execute(stmt)
        except IntegrityError:
            raise UniqueObjectException
        await self.session.commit()
        return self.mapper.map_to_schemas_object(result.scalars().one())

    async def edit(self,
                   data: BaseModel,
                   exclude_unset: bool = False,
                   **filter_by):
        """Обновляет существующую запись.

                Args:
                    data (BaseModel): Pydantic-схема с данными для обновления.
                    exclude_unset (bool): Если True, обновляются только переданные поля.
                    **filter_by: Параметры фильтрации (например, `id=1`).

                Returns:
                    BaseModel: Обновленный объект.

                Raises:
                    ObjectNotFoundException: Если объект не найден.
                    UniqueObjectException: Если нарушено ограничение уникальности.
        """
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model))
        try:
            result = await self.session.execute(stmt)
            edit_model = result.scalars().one()
            await self.session.commit()
        except (IntegrityError, NoResultFound) as ex:
            if isinstance(ex, IntegrityError):
                raise UniqueObjectException
            raise ObjectNotFoundException

        return self.mapper.map_to_schemas_object(edit_model)

    async def delete(self, **filter_by):
        """Удаляет запись из БД.

                Args:
                    **filter_by: Параметры фильтрации (например, `id=1`).

                Returns:
                    int: ID удаленного объекта.

                Raises:
                    ObjectNotFoundException: Если объект не найден.
        """
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model.id)
        try:
            result = await self.session.execute(stmt)
            deleted_obj = result.scalars().one()
            await self.session.commit()
            return deleted_obj
        except NoResultFound:
            raise ObjectNotFoundException
