import pytest
import pytest_asyncio
from src.core.constants.departments import DepartmentsConst
from src.db.manager import DBManager
from src.models.departments import DepartmentsORM
from src.schemas.departments import SDepartmentsCreate


@pytest.fixture
def valid_department_dicts() -> list[dict]:
    return [
        {'name': 'HR Department', 'parent_id': None},
        {'name': 'IT Department', 'parent_id': None},
        {'name': 'Marketing Department', 'parent_id': None},
    ]


@pytest.fixture
def invalid_department_dicts() -> list[dict]:
    too_long_name = 'X' * (DepartmentsConst.NAME_MAX_LEN + 1)
    return [
        {'name': '', 'parent_id': None},
        {'name': too_long_name, 'parent_id': None},
        {'name': 'QA Team', 'parent_id': -5},
    ]


@pytest_asyncio.fixture(scope='function', loop_scope='function')
async def sample_departments(
    db_session: DBManager, valid_department_dicts: list[dict]
) -> list[DepartmentsORM]:
    created_departments = []
    async with db_session as manager:
        for dept_dict in valid_department_dicts[:2]:
            schema = SDepartmentsCreate(**dept_dict)
            orm_obj = await manager.departments.add_one(schema)
            created_departments.append(orm_obj)
        return created_departments
