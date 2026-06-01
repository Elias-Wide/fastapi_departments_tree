from typing import Dict, List

from sqlalchemy import literal, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased, selectinload

from src.core.constants.departments import DepartmentsConst
from src.core.exceptions.database import (
    DatabaseError,
)
from src.core.exceptions.services.departments import (
    DepartmentCycleError,
    DepartmentSelfReferenceError,
)
from src.core.logging import get_logger
from src.core.messages.services.departments import (
    DepartmentsErrorMessages,
    DepartmentsLogMessages,
)
from src.models.departments import DepartmentsORM
from src.repositories.base import SQLAlchemyRepository
from src.schemas.departments import SDepartmentsCreate, SDepartmentsUpdate

logger = get_logger(__name__)


class DepartmentsRepo(SQLAlchemyRepository):
    """Repository for managing Department records.

    Inherits core CRUD operations and implements custom recursive
    Common Table Expressions (CTE) for tree traversal and hierarchy
    validation.
    """

    model = DepartmentsORM

    async def add_one(
        self, department_data: SDepartmentsCreate
    ) -> DepartmentsORM:
        """Add a new department to the database.

        Args:
            department_data: Validated data for creating a department.

        Returns:
            DepartmentsORM: The created department record.
        """
        obj = await super().add_one(department_data)
        department_with_sub_departments = await self.get_department_hierarchy(
            department_id=obj.id,
            depth=DepartmentsConst.MAX_DEPTH,
            include_employees=False,
        )
        self._validate_tree_hierarchy(
            department_id=obj.id,
            new_parent_id=department_data.parent_id,
            sub_departments=department_with_sub_departments,
        )
        await self.session.commit()
        return obj

    async def delete(self, department: DepartmentsORM) -> None:
        """Delete a department from the database.

        Performs cascade deletion of all descendant departments.

        Args:
            department: The department record to delete.
        """
        await super().delete(department)
        await self.session.commit()

    async def update(
        self, department: DepartmentsORM, update_data: SDepartmentsUpdate
    ) -> DepartmentsORM:
        """Update an existing department's details and trigger check."""
        if update_data.parent_id:
            sub_departments = await self.get_department_hierarchy(
                department_id=department.id,
                depth=DepartmentsConst.MAX_DEPTH,
                include_employees=False,
            )
            self._validate_tree_hierarchy(
                department_id=department.id,
                new_parent_id=update_data.parent_id,
                sub_departments=sub_departments,
            )
        department = await super().update(department, update_data)
        await self.session.commit()
        return department

    async def get_with_employees(self, department_id: int) -> DepartmentsORM:
        """Retrieve a department along with its employees via selectinload."""
        try:
            query = (
                select(self.model)
                .filter(self.model.id == department_id)
                .options(selectinload(self.model.employees))
            )
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            msg = DepartmentsLogMessages.LOG_GET_DEPT_WITH_EMP_ERR
            logger.error(msg.format(dept_id=department_id, error=e))
            raise DatabaseError(
                DepartmentsErrorMessages.ERR_GET_DEPT_WITH_EMP_FAILED
            ) from e

    async def get_department_hierarchy(
        self,
        department_id: int,
        depth: int,
        include_employees: bool = False,
    ) -> List[DepartmentsORM]:
        """Recursively fetch a department tree up to a specified depth.

        Args:
            department_id: The ID of the root department.
            depth: The maximum depth of the recursive tree search.
            include_employees: If True, eager loads employees relation.

        Returns:
            A list of departments matching the hierarchy criteria.
        """
        base_cte = select(self.model.id, literal(1).label('depth')).where(
            self.model.id == department_id
        )
        cte = base_cte.cte(name='department_tree_cte', recursive=True)

        recursive_alias = aliased(self.model)
        recursive_query = select(
            recursive_alias.id, (cte.c.depth + 1).label('depth')
        ).join(recursive_alias, recursive_alias.parent_id == cte.c.id)
        recursive_query = recursive_query.where(cte.c.depth < depth)
        cte_statement = cte.union_all(recursive_query)

        final_query = select(self.model).join(
            cte_statement, self.model.id == cte_statement.c.id
        )

        if include_employees:
            final_query = final_query.options(
                selectinload(self.model.employees)
            )

        result = await self.session.execute(final_query)
        return list(result.scalars().all())

    async def _get_department_full_hierarchy(
        self,
        department_id: int,
    ) -> Dict[str, List[int]]:
        """Collect sub-department and employee IDs required for deletion logic.

        Args:
            department_id: The ID of the department.

        Returns:
            A dictionary containing lists of sub-department IDs and
            transferable employee IDs.
        """
        departments = await self.get_department_hierarchy(
            department_id=department_id,
            depth=DepartmentsConst.MAX_DEPTH,
            include_employees=True,
        )

        sub_department_ids = [
            d.id for d in departments if d.id != department_id
        ]

        employee_ids = [
            emp.id
            for d in departments
            if d.id != department_id
            for emp in d.employees
        ]

        return {
            'sub_department_ids': sub_department_ids,
            'employee_ids': employee_ids,
        }

    def _validate_tree_hierarchy(
        self,
        department_id: int,
        new_parent_id: int,
        sub_departments: List[DepartmentsORM],
    ) -> None:
        """Validate that the new parent does not cause issues."""
        if department_id == new_parent_id:
            raise DepartmentSelfReferenceError()
        sub_departments_ids = {obj.id for obj in sub_departments}
        if new_parent_id in sub_departments_ids:
            msg = DepartmentsLogMessages.LOG_DEPT_CYCLE_ERR
            logger.error(
                msg.format(
                    dept_id=department_id,
                    new_parent_id=new_parent_id,
                )
            )
            raise DepartmentCycleError()
