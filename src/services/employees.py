from typing import List, Optional

from src.core.exceptions.services.employees import EmployeeNotFoundError
from src.schemas.employees import SEmployeeAdd, SEmployees
from src.services.base import BaseService


class EmployeesService(BaseService):
    """
    Service layer responsible for managing employee business logic.

    All business checks and transaction control via DBManager
    are encapsulated within this layer.
    """

    async def add_one(self, employee_data: SEmployeeAdd) -> SEmployees:
        """
        Hire a new employee into a specific department.

        Validates the target department existence before creation.

        Args:
            employee_data: Pydantic schema containing employee details.

        Returns:
            SEmployees: The newly created employee record.
        """
        employee = await self.db.employees.add_one(employee_data)
        return SEmployees.model_validate(employee)

    async def get_all_employees(self) -> List[SEmployees]:
        """
        Retrieve a list of all active employees in the company.

        Returns:
            List[SEmployees]: A list of all validated records.
        """
        employees = await self.db.employees.get_all()
        return [SEmployees.model_validate(emp) for emp in employees]

    async def get_employee_by_id(
        self, employee_id: int
    ) -> Optional[SEmployees]:
        """
        Find a specific employee by their unique identifier.

        Args:
            employee_id: The ID of the employee to look up.

        Returns:
            Optional[SEmployees]: Validated record or None.
        """
        employee = await self.db.employees.get_one_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError()
        return SEmployees.model_validate(employee)

    async def delete_employee(self, employee_id: int) -> None:
        """
        Terminate an employee's contract and remove their record.

        Args:
            employee_id: The ID of the employee to delete.
        """
        employee = await self.db.employees.get_one_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError()
        await self.db.employees.delete(employee)

    async def move_employees_to_department(
        self, employees_ids: List[int], new_department_id: int
    ) -> None:
        """
        Transfer an employee to a different department.

        Validates the employee and target department before updating.

        Args:
            employee_id: The ID of the employee being moved.
            new_department_id: The destination department ID.
        """
        await self.db.employees.bulk_change_department
