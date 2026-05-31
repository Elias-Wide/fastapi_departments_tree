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

    async def move_employees_to_department(
        self, old_department_id: int, new_department_id: int
    ) -> None:
        """
        Move all employees from one department to another.

        Args:
            old_department_id: The ID of the department to move employees from.
            new_department_id: The ID of the department to move employees to.
        """
        query = (
            self.model.__table__.update()
            .where(self.model.department_id == old_department_id)
            .values(department_id=new_department_id)
        )
        await self.session.execute(query)
        await self.session.commit()
