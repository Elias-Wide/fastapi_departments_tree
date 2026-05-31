from typing import AsyncGenerator

from sqlalchemy import Column, Integer, NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)

from src.config import settings

if settings.app.mode == 'TEST':
    DATABASE_URL = settings.db.test_url
    DATABASE_PARAMS = {'poolclass': NullPool}
if settings.app.mode == 'DEV':
    DATABASE_URL = settings.db.url
    DATABASE_PARAMS = {'echo': True}
else:
    DATABASE_URL = settings.db.url
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

SessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


class PreBase:
    """Base class for all ORM models with common attrs and methods."""

    @declared_attr
    def __tablename__(self) -> str:
        """Returns the table name for the model in lowercase"""
        return self.__name__.lower()[:-3]  # Remove Orm suffix

    id = Column(Integer, primary_key=True)


class Model(DeclarativeBase, PreBase):
    pass


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def drop_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
