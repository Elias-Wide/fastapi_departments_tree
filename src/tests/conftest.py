import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.db.database import Model, SessionLocal, engine
from src.db.manager import DBManager
from src.dependencies.db_manager import get_db_manager
from src.main import app
from src.tests.fixtures.departments import *  # noqa: F403, F401
from src.tests.fixtures.employess import *  # noqa: F403, F401

os.environ['APP_MODE'] = 'TEST'


@pytest_asyncio.fixture(scope='session', loop_scope='session', autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope='function', loop_scope='function')
async def db_session() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=SessionLocal) as manager:
        yield manager
    async with engine.begin() as conn:
        for table in reversed(Model.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest_asyncio.fixture(scope='function', loop_scope='function')
async def client(
    db_session: DBManager,
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db_manager():
        yield db_session

    app.dependency_overrides[get_db_manager] = override_get_db_manager
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def main_api_route() -> str:
    return '/api/v1'


@pytest.fixture
def departments_base_route(main_api_route: str) -> str:
    return f'{main_api_route}/departments'


@pytest.fixture
def department_id_route(departments_base_route: str) -> str:
    return f'{departments_base_route}/{{department_id}}'


@pytest.fixture
def department_employees_route(department_id_route: str) -> str:
    return f'{department_id_route}/employees'
