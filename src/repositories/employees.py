from typing import List

from sqlalchemy import update

from src.models.employees import EmployeesORM
from src.repositories.base import SQLAlchemyRepository
from src.schemas.employees import SEmployees


class EmployeesRepo(SQLAlchemyRepository[EmployeesORM, SEmployees]):
    """
    Repository for managing Employee records.

    Inherits core CRUD operations and implements batch filtering
    utilities to support decoupled department-employee operations.
    """

    model = EmployeesORM

    async def add_one(self, employee_data: SEmployees) -> EmployeesORM:
        """
        Add a new employee to the database.

        Args:
            employee_data: Validated data for creating an employee.

        Returns:
            EmployeesORM: The created employee record.
        """
        obj = await super().add_one(employee_data)
        await self.session.commit()
        return obj

    async def bulk_change_department(
        self, employee_ids: List[int], new_department_id: int
    ) -> None:
        """Move multiple employees to a different department.

        Args:
            employee_ids: A list of employee IDs to be transferred.
            new_department_id: The ID of the department to move employees to.
        """
        statement = (
            update(self.model)
            .where(self.model.id.in_(employee_ids))
            .values(department_id=new_department_id)
        )
        await self.session.execute(statement)
