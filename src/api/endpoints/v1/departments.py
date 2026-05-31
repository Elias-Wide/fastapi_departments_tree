from typing import Annotated, Union

from fastapi import APIRouter, Depends, status

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
async def add_one(
    db: DBManagerDep, department: Annotated[SDepartmentsCreate, Depends()]
):
    service = DepartmentsService(db)
    new_department = await service.add_one(department)
    return SDepartmentsResponse.model_validate(new_department)


@router.get(
    '/',
    response_model=list[SDepartmentsResponse, SDepartmentsResponseExtended],
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
    service = DepartmentsService(db)
    await service.delete_department(department_id, **delete_params)


@router.post(
    '/{department_id}/employees',
    response_model=SEmployeesResponse,
    summary='Add an employee to the department',
)
async def add_one_to_department(
    db: DBManagerDep,
    department_id: int,
    employee: Annotated[SEmployeesCreate, Depends()],
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
    department_data: Annotated[SDepartmentsUpdate, Depends()],
):
    service = DepartmentsService(db)
    await service.update_department(department_id, department_data)
