from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import SessionLocal, get_session
from src.db.manager import DBManager

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_db_manager() -> AsyncGenerator[DBManager, None]:
    async with DBManager(SessionLocal) as manager:
        yield manager


DBManagerDep = Annotated[DBManager, Depends(get_db_manager)]
