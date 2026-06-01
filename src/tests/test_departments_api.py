import pytest
from httpx import AsyncClient

from src.models.departments import DepartmentsORM


@pytest.mark.asyncio
async def test_department_success(
    client: AsyncClient,
    departments_base_route: str,
    valid_department_dicts: list[dict],
) -> None:
    payload = valid_department_dicts[0]
    response = await client.post(departments_base_route, json=payload)
    assert response.status_code == 201
    assert response.json()['name'] == payload['name']


@pytest.mark.asyncio
async def test_add_one_validation_error(
    client: AsyncClient,
    departments_base_route: str,
    invalid_department_dicts: list[dict],
) -> None:
    pass


@pytest.mark.asyncio
async def test_get_all_departments(
    client: AsyncClient,
    departments_base_route: str,
    sample_departments: list[DepartmentsORM],
) -> None:
    pass

@pytest.mark.asyncio
async def test_get_department_by_id(
    client: AsyncClient,
    department_id_route: str,
    sample_departments: list[DepartmentsORM],
) -> None:
    pass

@pytest.mark.asyncio
async def test_update_department_success(
    client: AsyncClient,
    department_id_route: str,
    sample_departments: list[DepartmentsORM],
) -> None:
    pass

@pytest.mark.asyncio
async def test_update_department_validation_error(
    client: AsyncClient,
    department_id_route: str,
    sample_departments: list[DepartmentsORM],
    invalid_department_dicts: list[dict],
) -> None:
    pass

@pytest.mark.asyncio
async def test_add_one_to_department(
    client: AsyncClient,
    department_employees_route: str,
    sample_departments: list[DepartmentsORM],
) -> None:
    pass

@pytest.mark.asyncio
async def test_delete_department(
    client: AsyncClient,
    department_id_route: str,
    sample_departments: list[DepartmentsORM],
) -> None:
    pass