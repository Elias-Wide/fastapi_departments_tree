from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import SessionLocal
from src.repositories.departments import DepartmentsRepo
from src.repositories.employees import EmployeesRepo


class DBManager:
    """
    Manager for handling database sessions and repository access.
    """

    def __init__(
        self, session_factory: Callable[[], AsyncSession] = SessionLocal
    ):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self.departments: DepartmentsRepo | None = None
        self._committed = False

    async def __aenter__(self) -> 'DBManager':
        self.session = self.session_factory()
        self.departments = DepartmentsRepo(self.session)
        self.employees = EmployeesRepo(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Gracefully close the session.
        Rolls back only if an exception occurred.
        """
        try:
            if exc_type or not self._committed:
                await self.session.rollback()
        finally:
            await self.session.close()

    async def commit(self) -> None:
        """
        Explicitly save changes.
        This should be called at the end of successful logic.
        """
        if self.session:
            await self.session.commit()
            self._committed = True
