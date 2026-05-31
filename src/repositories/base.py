from typing import Any, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database import (
    DatabaseError,
    DBForeignKeyViolationError,
)
from src.core.logging import get_logger
from src.core.messages.database import DbErrorMessages, DbLogMessages
from src.db.database import Model

logger = get_logger(__name__)

ModelType = TypeVar('ModelType', bound=Model)
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class SQLAlchemyRepository(Generic[ModelType, SchemaType]):
    """Base repository class for common database operations."""

    model: Type[ModelType] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, model_data: SchemaType) -> ModelType:
        """Create a new record."""
        try:
            model_dict = model_data.model_dump()
            model_obj = self.model(**model_dict)
            self.session.add(model_obj)
            await self.session.flush()
            return model_obj
        except IntegrityError as e:
            logger.error(DbLogMessages.LOG_INTEGRITY_ERR.format(error=e))
            raise DBForeignKeyViolationError(
                DbErrorMessages.ERR_FOREIGN_KEY_VIOLATION
            ) from e
        except SQLAlchemyError as e:
            logger.error(DbLogMessages.LOG_INSERT_ERR.format(error=e))
            raise DatabaseError(DbErrorMessages.ERR_INSERT_FAILED) from e

    async def get_all(self) -> List[SchemaType]:
        """Retrieve all records."""
        try:
            query = select(self.model)
            result = await self.session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(DbLogMessages.LOG_FETCH_ERR.format(error=e))
            raise DatabaseError(DbErrorMessages.ERR_FETCH_FAILED) from e

    async def get_one_by_id(self, pk: int) -> Optional[ModelType]:
        """Retrieve a single record by its ID."""
        return await self.get_one_by_field('id', pk)


    async def get_one_by_field(
        self, attr_name: str, attr_value: Any
    ) -> Optional[SchemaType]:
        """Generic filter for a single record."""
        query = select(self.model).where(
            getattr(self.model, attr_name) == attr_value
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(self, db_obj: ModelType, obj_in: SchemaType) -> ModelType:
        """Update an object in the current session context."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def delete(self, db_obj: ModelType) -> None:
        """Mark an object for deletion."""
        try:
            await self.session.delete(db_obj)
            await self.session.flush()
        except SQLAlchemyError as e:
            logger.error(DbLogMessages.LOG_DELETE_ERR.format(error=e))
            raise DatabaseError(DbErrorMessages.ERR_DELETE_FAILED) from e
