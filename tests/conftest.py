from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from iu_carrige.api.core import app
from pytest import fixture
from uuid import uuid4


@fixture(scope='session')
async def client():
    async with LifespanManager(app) as manager:
        async with AsyncClient(base_url='http://localhost:8000', app=manager.app) as client:
            yield client


@fixture(scope='class')
def hash_data():
    return uuid4().hex
