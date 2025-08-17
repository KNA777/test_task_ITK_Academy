from src.repositories.books import BooksRepository


class DBManager:
    """Менеджер для работы с асинхронными сессиями базы данных.

        Обеспечивает централизованное управление репозиториями и транзакциями.
        Реализует контекстный менеджер через __aenter__/__aexit__ для автоматического
        управления жизненным циклом сессии.

        Attributes:
            session_factory: Фабрика для создания асинхронных сессий SQLAlchemy.
            session: Текущая активная сессия БД.
            books: Репозиторий для работы с книгами.
    """

    def __init__(self, session_factory):
        """Инициализирует менеджер с фабрикой сессий.

                Args:
                    session_factory: Callable, создающий новый экземпляр AsyncSession.
        """
        self.session_factory = session_factory

    async def __aenter__(self):
        """Вход в контекстный менеджер. Создает сессию и инициализирует репозитории.

                Returns:
                    self: Экземпляр DBManager с активной сессией.
        """
        self.session = self.session_factory()

        self.books = BooksRepository(self.session)

        return self

    async def __aexit__(self, *args):
        """Выход из контекстного менеджера. Откатывает и закрывает сессию.

                Args:
                    *args: Аргументы исключения (type, value, traceback), если оно возникло.
        """
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        """Фиксирует текущую транзакцию в БД.

                Raises:
                    SQLAlchemyError: При ошибках во время коммита.
        """
        self.session.commit()
