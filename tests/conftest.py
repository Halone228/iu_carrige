from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from iu_carrige.api.core import app
from pytest import fixture
from uuid import uuid4
from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory
from iu_datamodels import MineralAndAttachments, SourceShort, Vein, MineralAndAttachmentsShort

faker_ = Faker()


class VeinFactory(ModelFactory[Vein]):
    __model__ = Vein


class SourceFactory(ModelFactory[SourceShort]):
    __model__ = SourceShort


class MineralFactory(ModelFactory[MineralAndAttachmentsShort]):
    __model__ = MineralAndAttachmentsShort


@fixture(scope='session')
async def client():
    async with LifespanManager(app) as manager:
        async with AsyncClient(base_url='http://localhost:8000', transport=ASGITransport(app=manager.app)) as client:
            yield client


@fixture(scope='class')
def hash_data():
    return uuid4().hex


@fixture(scope='class')
def gen_vein() -> Vein:
    return VeinFactory.build()


@fixture(scope='class')
def gen_source(gen_vein: Vein):
    source: SourceShort = SourceFactory.build()
    return source


@fixture(scope='class')
def gen_mineral():
    return MineralFactory.build()
