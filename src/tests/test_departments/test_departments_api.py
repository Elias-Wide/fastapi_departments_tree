import pytest
from httpx import AsyncClient
from src.core.constants.departments import DepartmentsConst


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
@pytest.mark.parametrize(
    'payload, expected_status',
    [
        ({'name': '', 'parent_id': None}, 422),
        (
            {
                'name': 'X' * (DepartmentsConst.NAME_MAX_LEN + 1),
                'parent_id': None,
            },
            422,
        ),
        ({'name': 'QA Team', 'parent_id': -5}, 422),
    ],
)
async def test_add_one_validation_error(
    client: AsyncClient,
    departments_base_route: str,
    payload: dict,
    expected_status: int,
) -> None:
    response = await client.post(departments_base_route, json=payload)
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_get_all_departments(
    client: AsyncClient,
    departments_base_route: str,
    sample_departments: list,
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
    sample_departments: list,
) -> None:
    target_id = sample_departments[0].id
    url = f'departments/{target_id}'
    params = {'depth': 1}
    response = await client.get(url, params=params)
    assert response.status_code == 200
    assert response.json()['id'] == target_id


@pytest.mark.asyncio
async def test_update_department_success(
    client: AsyncClient,
    sample_departments: list,
) -> None:
    target_id = sample_departments[0].id
    url = f'departments/{target_id}'
    payload = {'name': 'R&D Engineering'}
    response = await client.patch(url, json=payload)
    assert response.status_code == 200
    assert response.json()['name'] == 'R&D Engineering'


@pytest.mark.asyncio
async def test_update_department_validation_error(
    client: AsyncClient,
    sample_departments: list,
) -> None:
    target_id = sample_departments[0].id
    url = f'departments/{target_id}'
    payload = {'name': 'X' * (DepartmentsConst.NAME_MAX_LEN + 1)}
    response = await client.patch(url, json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_one_to_department(
    client: AsyncClient,
    sample_departments: list,
) -> None:
    target_id = sample_departments[0].id
    url = f'departments/{target_id}/employees'
    payload = {
        'full_name': 'Jane Smith',
        'position': 'QA Engineer',
    }
    response = await client.post(url, json=payload)
    assert response.status_code == 201
    assert response.json()['full_name'] == 'Jane Smith'
