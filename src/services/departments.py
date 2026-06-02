from typing import Dict, List, Optional, Union

from src.core.constants.departments import DepartmentsConst
from src.core.exceptions.database import (
    DatabaseError,
    DbDepartmentSelfReferenceError,
    DBForeignKeyViolationError,
    DBUniqueViolationError,
)
from src.core.exceptions.services.departments import (
    DepartmentAlreadyExistsError,
    DepartmentCycleError,
    DepartmentNotFoundError,
    DepartmentSelfReferenceError,
    DepartmentServiceError,
)
from src.core.logging import get_logger
from src.core.messages.services.departments import (
    DepartmentsErrorMessages,
    DepartmentsLogMessages,
)
from src.models.departments import DepartmentsORM
from src.schemas.departments import (
    SDepartments,
    SDepartmentsCreate,
    SDepartmentsResponse,
    SDepartmentsResponseExtended,
    SDepartmentsTreeResponse,
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

    async def add_one(
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
            raise DepartmentAlreadyExistsError(
                DepartmentsErrorMessages.ERR_UQ_DEPT_NAME_BY_PARENT.format(
                    name=department_data.name,
                )
            ) from e
        except DBForeignKeyViolationError as e:
            raise (DepartmentsErrorMessages.FK_PARENT_DEPT_NOT_FOUND) from e
        except DbDepartmentSelfReferenceError as e:
            logger.error(
                DepartmentsLogMessages.LOG_CREATE_DEPT_SELF_PARENT_ERR.format(
                    dept_id=department_data.parent_id
                )
            )
            raise DepartmentSelfReferenceError(
                DepartmentsErrorMessages.ERR_CREATE_DEPT_SELF_PARENT
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
            List[SDepartmentsResponse]: A list of all validated records.
        """
        departments = await self.db.departments.get_all()
        return [
            SDepartmentsResponse.model_validate(dept) for dept in departments
        ]

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
        department = await self.db.departments.get_one_by_id(pk=department_id)
        if not department:
            raise DepartmentNotFoundError()
        updated_department = await self.db.departments.update(
            department, department_data
        )
        return SDepartmentsResponse.model_validate(updated_department)

    async def delete_department(
        self,
        department_id: int,
    ) -> None:
        """
        Remove a department record along with its whole branch.

        Triggers a cascade delete for all sub-departments and
        associated employees via DB rules.
        Args:
            department_id: The ID of the department to delete.
        """
        department = await self.db.departments.get_one_by_id(department_id)
        if not department:
            raise DepartmentNotFoundError()
        await self.db.departments.delete(department)

    async def _check_department_tree_validity(
        self,
        department_id: int,
        new_parent_id: Optional[int],
        departments_lst: List[DepartmentsORM],
    ) -> None:
        """
        Validate that moving a department does not create a cyclical tree.

        Recursively checks the ancestry of the target parent department
        to ensure it does not reference the department being moved.

        Args:
            department_id: The ID of the department being moved.
            new_parent_id: The ID of the proposed new parent department.
            deps_list: List of the department and his children.
        """
        if department_id == new_parent_id:
            raise DepartmentSelfReferenceError()
        if new_parent_id in list(obj.id for obj in departments_lst):
            logger.error(
                DepartmentsLogMessages.LOG_DEPT_CYCLE_ERR.format(
                    dept_id=department_id, new_parent_id=new_parent_id
                )
            )
            raise DepartmentCycleError()
        return True

    async def get_department_by_id(
        self,
        department_id: int,
        depth: int = DepartmentsConst.MIN_DEPTH,
        include_employees: bool = True,
    ) -> Union[
        SDepartmentsResponse,
        SDepartmentsResponseExtended,
        SDepartmentsTreeResponse,
    ]:
        """Retrieve a department by ID and build a tree structure[Optional]"""
        if depth == DepartmentsConst.MIN_DEPTH:
            get_department = (
                self.db.departments.get_with_employees
                if include_employees
                else self.db.departments.get_one_by_id
            )
            db_dept = await get_department(department_id)
            if not db_dept:
                raise DepartmentNotFoundError()

            response_model = (
                SDepartmentsResponseExtended
                if include_employees
                else SDepartmentsResponse
            )
            return response_model.model_validate(db_dept)

        departments: List[
            DepartmentsORM
        ] = await self.db.departments.get_department_hierarchy(
            department_id, depth, include_employees
        )
        if not departments:
            raise DepartmentNotFoundError()
        return self._build_department_tree(
            departments, department_id, include_employees
        )

    def _build_department_tree(
        self,
        departments: List[DepartmentsORM],
        root_id: int,
        include_employees: bool,
    ) -> SDepartmentsTreeResponse:
        """Build a Pydantic tree model from a flat list of ORM departments."""
        nodes: Dict[int, SDepartmentsTreeResponse] = {}
        for orm_dept in departments:
            current_employees = None
            if include_employees:
                extended_dto = SDepartmentsResponseExtended.model_validate(
                    orm_dept
                )
                current_employees = extended_dto.employees

            node_schema = SDepartmentsTreeResponse(
                id=orm_dept.id,
                name=orm_dept.name,
                parent_id=orm_dept.parent_id,
                created_at=orm_dept.created_at,
                employees=current_employees,
                children=[],
            )
            nodes[node_schema.id] = node_schema

        root_node = None
        for item in nodes.values():
            if item.id == root_id:
                root_node = item
            parent_id = item.parent_id
            if parent_id in nodes and item.id != root_id:
                nodes[parent_id].children.append(item)
        if not root_node:
            root_node = nodes.get(root_id)
        if not root_node:
            raise DepartmentNotFoundError()
        return root_node
