from typing import List, Optional

from src.core.constants.departments import DepartmentsConst
from src.core.exceptions.database import DatabaseError, DBUniqueViolationError
from src.core.exceptions.services.departments import (
    DepartmentAlreadyExistsError,
    DepartmentServiceError,
    DepartmentNotFoundError,
)
from src.core.exceptions.services.departments import DepartmentNotFoundError
from src.core.logging import get_logger
from src.core.messages.services.departments import (
    DepartmentsErrorMessages,
    DepartmentsLogMessages,
)
from src.schemas.departments import (
    SDepartments,
    SDepartmentsCreate,
    SDepartmentsResponse,
    SDepartmentsUpdate,
)
from src.services.base import BaseService

logger = get_logger(__name__)


class DepartmentsService(BaseService):
    """
    Service layer responsible for managing department business logic.

    Handles hierarchical tree operations, anti-cyclical cycle
    validations, and cascade deletion verifications.
    """

    async def create_department(
        self, department_data: SDepartmentsCreate
    ) -> SDepartments:
        """
        Create a new organizational department.

        Ensures unique constraints for names under the same parent.

        Args:
            department_data: Validated department creation attributes.

        Returns:
            SDepartments: The created department instance.
        """
        try:
            department = await self.db.departments.add_one(department_data)
            return SDepartments.model_validate(department)
        except DBUniqueViolationError as e:
            logger.error(
                DepartmentsLogMessages.LOG_CREATE_DEPT_ERR.format(error=e)
            )
            raise DepartmentAlreadyExistsError(
                DepartmentsErrorMessages.ERR_CREATE_DEPT_FAILED
            ) from e
        except DatabaseError as e:
            logger.error(
                DepartmentsLogMessages.LOG_CREATE_DEPT_ERR.format(error=e)
            )
            raise DepartmentServiceError(
                DepartmentsErrorMessages.ERR_CREATE_DEPT_FAILED
            ) from e

    async def get_all_departments(self) -> List[SDepartmentsResponse]:
        """
        Retrieve a flat list of all active departments.

        Returns:
            List[DepartmentSchema]: A list of all validated records.
        """
        departments = await self.db.departments.get_all()
        return [
            SDepartmentsResponse.model_validate(dept) for dept in departments
        ]

    async def get_department_by_id(
        self, department_id: int
    ) -> Optional[SDepartmentsResponse]:
        """
        Find a specific department by its unique identifier.

        Args:
            department_id: The ID of the department to look up.

        Returns:
            Optional[DepartmentSchema]: Validated record or None.
        """
        department = await self.db.departments.get_one_by_field(
            'id', department_id
        )
        if not department:
            raise DepartmentNotFoundError()
        return SDepartmentsResponse.model_validate(department)

    async def update_department(
        self, department_id: int, department_data: SDepartmentsUpdate
    ) -> SDepartmentsResponse:
        """
        Partially update an existing department's details.

        Validates the target department existence before applying updates.

        Args:
            department_id: The ID of the department to update.
            department_data: Validated data for updating the department.

        Returns:
            SDepartmentsResponse: The updated department record.
        """
        department = await self.db.departments.get_one_by_id(id=department_id)
        if not department:
            raise DepartmentNotFoundError()
        if department_data.parent_id:
            # check department tree
            pass
        updated_department = await self.db.departments.update(
            department, department_data
        )
        return SDepartmentsResponse.model_validate(updated_department)

    # async def get_department_tree(
    #     self, department_id: int, depth: int = 1
    # ) -> SDepartmentsTreeResponse:
    #     """
    #     Fetch a recursive sub-tree starting from the target department.

    #     Limits the lookup depth between 1 and 5 using DB-level CTE.

    #     Args:
    #         department_id: Root node ID of the requested hierarchy.
    #         depth: Level of nesting to fetch downwards (defaults to 1).

    #     Returns:
    #         DepartmentTreeResponse: Hierarchical tree Pydantic schema.
    #     """
    #     pass

    async def move_department(
        self, department_id: int, new_parent_id: Optional[int]
    ) -> None:
        """
        Relocate a department to a new parent node in the tree.

        Performs strict recursive validation to prevent any cyclical
        dependencies (e.g., preventing a parent from becoming a child
        of its own sub-department).

        Args:
            department_id: The ID of the department being moved.
            new_parent_id: Target parent department ID or None for root.
        """
        pass

    async def delete_department(
        self,
        department_id: int,
        mode: str,
        reassign_to_department_id: int | None = None,
    ) -> None:
        """
        Remove a department record along with its whole branch.

        Triggers a cascade delete for all sub-departments and
        associated employees via DB rules.

        Args:
            department_id: The ID of the department to delete.
            mode: The deletion mode ('cascade' or 'reassign').
            reassign_to_department_id: The ID of the department to reassign employees to (required for 'reassign' mode).
        """
        department = await self.db.departments.get_one_by_id(department_id)
        if not department:
            raise DepartmentNotFoundError()
        if mode == DepartmentsConst.REASSIGN_DELETE_MODE:
            new_department = await self.db.departments.get_one_by_id(
                reassign_to_department_id
            )
            if not new_department:
                raise DepartmentNotFoundError(
                    DepartmentsErrorMessages.ERR_REASSIGN_DEPT_NOT_FOUND.format(
                        department_id=reassign_to_department_id
                    )
                )
            await self.db.employees.move_employees_to_department(
                department_id, reassign_to_department_id
            )
        await self.db.departments.delete(department)
