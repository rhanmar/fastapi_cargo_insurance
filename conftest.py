import pytest
from fastapi.testclient import TestClient
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from main import app
from models import Cargo, Rate


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


async def init_test_db():
    register_tortoise(
        app,
        db_url="sqlite://sql_app_test.db",
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init_test_db()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(autouse=True)
async def clear_db() -> None:
    await Rate.all().delete()
    await Cargo.all().delete()
