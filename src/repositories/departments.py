from src.models.departments import DepartmentsORM
from src.repositories.base import SQLAlchemyRepository
from src.schemas.departments import SDepartmentsCreate, SDepartmentsUpdate


class DepartmentsRepo(SQLAlchemyRepository):
    """
    Repository for managing Department records.

    Inherits core CRUD operations and implements custom recursive
    Common Table Expressions (CTE) for tree traversal.
    """

    model = DepartmentsORM

    async def add_one(
        self, department_data: SDepartmentsCreate
    ) -> DepartmentsORM:
        """
        Add a new department to the database.

        Args:
            department_data: Validated data for creating a department.

        Returns:
            DepartmentsORM: The created department record.
        """
        obj = await super().add_one(department_data)
        await self.session.commit()
        return obj

    async def delete(self, department: DepartmentsORM) -> None:
        """
        Delete a department from the database.

         Performs cascade deletion of all descendant departments.

         Args:
             department: The department record to delete.
        """
        await super().delete(department)
        await self.session.commit()

    async def update(
        self, department: DepartmentsORM, update_data: SDepartmentsUpdate
    ) -> DepartmentsORM:
        """Update an existing department's details."""
        department = await super().update(department, update_data)
        await self.session.commit()
        return department
