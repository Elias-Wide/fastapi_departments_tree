from fastapi import APIRouter

from src.dependencies.db_manager import DBManagerDep
from src.schemas.employees import SEmployeesResponse
from src.services.employees import EmployeesService


router = APIRouter(prefix='/employees', tags=['employees'])


@router.get('/', summary='Get all employees')
async def get_all_employees(db: DBManagerDep) -> list[SEmployeesResponse]:
    service = EmployeesService(db)
    return await service.get_all_employees()


@router.get('/{employee_id}', summary='Get employee by ID')
async def get_employee_by_id(
    db: DBManagerDep, employee_id: int
) -> SEmployeesResponse:
    service = EmployeesService(db)
    employee = await service.get_employee_by_id(employee_id)
    return SEmployeesResponse.model_validate(employee)
