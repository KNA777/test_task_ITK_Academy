from fastapi import Request
from typing import Annotated

from fastapi import Depends

from src.config.db_config import async_session
from src.config.db_context_manager import DBManager


async def get_db(request: Request):
    async with DBManager(session_factory=async_session) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
