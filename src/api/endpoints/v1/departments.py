from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response, status

from src.dependencies.db_manager import DBManagerDep
from src.dependencies.departments import (
    DeleteDepartmentParamsDep,
    get_department_delete_params,
)
from src.schemas.departments import (
    SDepartmentsCreate,
    SDepartmentsResponse,
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
async def create_department(
    db: DBManagerDep, department: Annotated[SDepartmentsCreate, Depends()]
):
    service = DepartmentsService(db)
    new_department = await service.create_department(department)
    return SDepartmentsResponse.model_validate(new_department)


@router.get(
    '/',
    response_model=list[SDepartmentsResponse],
    summary='Get all departments',
)
async def get_all_departments(db: DBManagerDep) -> list[SDepartmentsResponse]:
    service = DepartmentsService(db)
    return await service.get_all_departments()


@router.get(
    '/{department_id}',
    response_model=SDepartmentsResponse,
    summary='Get department by ID',
)
async def get_department(
    db: DBManagerDep, department_id: int
) -> SDepartmentsResponse:
    service = DepartmentsService(db)
    department = await service.get_department_by_id(department_id)
    return SDepartmentsResponse.model_validate(department)


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
async def add_employee_to_department(
    db: DBManagerDep,
    department_id: int,
    employee: Annotated[SEmployeesCreate, Depends()],
) -> SEmployeesResponse:
    departments_service = DepartmentsService(db)
    employees_service = EmployeesService(db)
    department = await departments_service.get_department_by_id(department_id)
    employee_data = employee.model_dump()
    employee_data['department_id'] = department.id
    new_employee = await employees_service.add_employee(
        SEmployeeAdd(**employee_data)
    )
    return SEmployeesResponse.model_validate(new_employee)


@router.patch(
    '/{department_id}',
    response_model=SDepartmentsResponse,
    summary='Partially update a department by ID',
)
async def update_department(
    db: DBManagerDep, department_id: int, department_data: SDepartmentsUpdate
):
    service = DepartmentsService(db)
    updated_department = await service.update_department(
        department_id, department_data
    )
