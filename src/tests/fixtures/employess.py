from datetime import date

import pytest
from src.db.manager import DBManager
from src.models.departments import DepartmentsORM
from src.models.employees import EmployeesORM


@pytest.fixture
def main_api_route() -> str:
    """Return the global API version prefix."""
    return '/api/v1'


@pytest.fixture
def departments_base_route(main_api_route: str) -> str:
    """Return the base route for departments endpoints."""
    return f'{main_api_route}/departments'


@pytest.fixture
def department_id_route(departments_base_route: str) -> str:
    """Return the route for a specific department with a template ID."""
    return f'{departments_base_route}/{{department_id}}'


@pytest.fixture
def department_employees_route(department_id_route: str) -> str:
    """Return the route for department employees with a template ID."""
    return f'{department_id_route}/employees'


@pytest.fixture
async def sample_department(db_session: DBManager) -> DepartmentsORM:
    """Create a sample department record in the database."""
    async with db_session.session_factory() as session:
        dept = DepartmentsORM(name='Engineering', parent_id=None)
        session.add(dept)
        await session.commit()
        await session.refresh(dept)

        return dept


@pytest.fixture
async def sample_employee(
    db_session: DBManager, sample_department: DepartmentsORM
) -> EmployeesORM:
    """Create a sample employee record linked to the sample department."""
    async with db_session.session_factory() as session:
        emp = EmployeesORM(
            full_name='John Doe',
            position='Software Engineer',
            hired_at=date(2026, 1, 1),
            department_id=sample_department.id,
        )
        session.add(emp)
        await session.commit()
        await session.refresh(emp)

        return emp
