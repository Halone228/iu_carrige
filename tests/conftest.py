from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from iu_carrige.api.core import app
from pytest import fixture


@fixture(scope='session')
async def client():
    async with LifespanManager(app) as manager:
        async with AsyncClient(base_url='http://localhost:8000', app=manager.app) as client:
            yield client
            