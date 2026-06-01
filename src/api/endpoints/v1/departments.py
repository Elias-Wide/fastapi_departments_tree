from typing import Union

from fastapi import APIRouter, status

from src.core.constants.departments import DepartmentsConst
from src.core.exceptions.services.departments import (
    DepartmentNotFoundError,
    DepartmentSelfReferenceError,
)
from src.core.messages.services.departments import DepartmentsErrorMessages
from src.dependencies.db_manager import DBManagerDep
from src.dependencies.departments import (
    DeleteDepartmentParamsDep,
    GetDepartmentSearchParamsDep,
)
from src.schemas.departments import (
    SDepartmentsCreate,
    SDepartmentsResponse,
    SDepartmentsResponseExtended,
    SDepartmentsTreeResponse,
    SDepartmentsUpdate,
)
from src.schemas.employees import (
    SEmployeeAdd,
    SEmployeesCreate,
    SEmployeesResponse,
)
from src.services.departments import DepartmentsService
from src.services.employees import EmployeesService

router = APIRouter(prefix='/departments', tags=['departments'])


@router.post(
    '',
    response_model=SDepartmentsResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Create a new department',
)
async def add_one(db: DBManagerDep, department: SDepartmentsCreate):
    service = DepartmentsService(db)
    new_department = await service.add_one(department)
    return SDepartmentsResponse.model_validate(new_department)


@router.get(
    '',
    response_model=list[SDepartmentsResponse],
    summary='Get all departments',
)
async def get_all_departments(db: DBManagerDep) -> list[SDepartmentsResponse]:
    service = DepartmentsService(db)
    return await service.get_all_departments()


@router.get(
    '/{department_id}',
    response_model=Union[
        SDepartmentsResponse,
        SDepartmentsResponseExtended,
        SDepartmentsTreeResponse,
    ],
    summary='Get department by ID',
)
async def get_department(
    db: DBManagerDep, department_id: int, params: GetDepartmentSearchParamsDep
) -> SDepartmentsResponse | SDepartmentsResponseExtended:
    service = DepartmentsService(db)
    return await service.get_department_by_id(department_id, **params)


@router.post(
    '/{department_id}/employees',
    response_model=SEmployeesResponse,
    summary='Add an employee to the department',
)
async def add_one_to_department(
    db: DBManagerDep,
    department_id: int,
    employee: SEmployeesCreate,
) -> SEmployeesResponse:
    departments_service = DepartmentsService(db)
    employees_service = EmployeesService(db)

    await departments_service.get_department_by_id(department_id)

    employee_data = employee.model_dump()
    employee_data['department_id'] = department_id

    new_employee = await employees_service.add_one(
        SEmployeeAdd(**employee_data)
    )
    return SEmployeesResponse.model_validate(new_employee)


@router.patch(
    '/{department_id}',
    response_model=SDepartmentsResponse,
    summary='Partially update a department by ID',
)
async def update_department(
    db: DBManagerDep,
    department_id: int,
    department_data: SDepartmentsUpdate,
):
    service = DepartmentsService(db)
    new_department = await service.update_department(
        department_id, department_data
    )
    return SDepartmentsResponse.model_validate(new_department)


@router.delete(
    '/{department_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete department by ID',
)
async def delete_department(
    db: DBManagerDep,
    department_id: int,
    delete_params: DeleteDepartmentParamsDep,
) -> None:
    mode = delete_params.get('mode')
    reassign_to_id = delete_params.get('reassign_to_department_id')
    departments_service = DepartmentsService(db)
    employees_service = EmployeesService(db)
    current_dept = await db.departments.get_one_by_id(department_id)
    if not current_dept:
        raise DepartmentNotFoundError()
    if mode == DepartmentsConst.REASSIGN_DELETE_MODE:
        if reassign_to_id == department_id:
            raise DepartmentSelfReferenceError(
                DepartmentsErrorMessages.ERR_DEL_DEPT_SAME_ID
            )
        target_dept = await db.departments.get_one_by_id(reassign_to_id)
        if not target_dept:
            raise DepartmentNotFoundError(
                DepartmentsErrorMessages.ERR_REASSIGN_DEPT_NOT_FOUND.format(
                    department_id=reassign_to_id
                )
            )
        context = await db.departments._get_department_full_hierarchy(
            department_id=department_id,
        )
        if reassign_to_id in context['sub_department_ids']:
            raise DepartmentSelfReferenceError(
                DepartmentsErrorMessages.ERR_REASSIGN_HIERARCHY
            )
        if context['employee_ids']:
            await employees_service.move_employees_to_department(
                employee_ids=context['employee_ids'],
                new_department_id=reassign_to_id,
            )
    await departments_service.delete_department(department_id)
    await db.commit()
