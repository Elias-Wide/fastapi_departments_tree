import pytest
from httpx import AsyncClient

from src.models.departments import DepartmentsORM


@pytest.mark.asyncio
async def test_add_one_success(
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
    payload = invalid_department_dicts[0]
    response = await client.post(departments_base_route, json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_departments(
    client: AsyncClient,
    departments_base_route: str,
    sample_departments: list[DepartmentsORM],
) -> None:
    response = await client.get(departments_base_route)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    target_id = sample_departments[0].id
    assert any(d['id'] == target_id for d in data)


@pytest.mark.asyncio
async def test_get_department_by_id(
    client: AsyncClient,
    department_id_route: str,
    sample_departments: list[DepartmentsORM],
) -> None:
    target_id = sample_departments[0].id
    url = department_id_route.format(department_id=target_id)
    params = {'include_extended': 'false'}
    response = await client.get(url, params=params)
    assert response.status_code == 200
    assert response.json()['id'] == target_id


@pytest.mark.asyncio
async def test_update_department_success(
    client: AsyncClient,
    department_id_route: str,
    sample_departments: list[DepartmentsORM],
) -> None:
    target_id = sample_departments[0].id
    url = department_id_route.format(department_id=target_id)
    payload = {'name': 'R&D Engineering'}
    response = await client.patch(url, json=payload)
    assert response.status_code == 200
    assert response.json()['name'] == 'R&D Engineering'


@pytest.mark.asyncio
async def test_update_department_validation_error(
    client: AsyncClient,
    department_id_route: str,
    sample_departments: list[DepartmentsORM],
    invalid_department_dicts: list[dict],
) -> None:
    target_id = sample_departments[0].id
    url = department_id_route.format(department_id=target_id)
    payload = {'name': invalid_department_dicts[1]['name']}
    response = await client.patch(url, json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_one_to_department(
    client: AsyncClient,
    department_employees_route: str,
    sample_departments: list[DepartmentsORM],
) -> None:
    target_id = sample_departments[0].id
    url = department_employees_route.format(department_id=target_id)
    payload = {
        'full_name': 'Jane Smith',
        'position': 'QA Engineer',
    }
    response = await client.post(url, json=payload)
    assert response.status_code == 200
    assert response.json()['full_name'] == 'Jane Smith'


@pytest.mark.asyncio
async def test_delete_department(
    client: AsyncClient,
    department_id_route: str,
    sample_departments: list[DepartmentsORM],
) -> None:
    target_id = sample_departments[0].id
    url = department_id_route.format(department_id=target_id)
    params = {'force': 'true'}
    response = await client.delete(url, params=params)
    assert response.status_code == 204
