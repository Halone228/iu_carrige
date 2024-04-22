import loguru
from httpx import AsyncClient
from pytest import mark
from iu_datamodels import VeinShort, SourceShort, MineralAndAttachments, MineralAndAttachmentsShort
from json import dumps
from base64 import b64encode
from uuid import uuid4
from pydantic import TypeAdapter


class TestMineral:
    stored_data = {}

    @mark.dependency(name="vein_create")
    async def test_create_vein(self, client: AsyncClient, gen_vein: VeinShort):
        response = await client.post(
            '/add_vein',
            json=gen_vein.model_dump()
        )
        assert response.status_code == 200, "Not success response"
        assert response.json()['created_id']
        TestMineral.stored_data['vein_id'] = response.json()['created_id']

    @mark.dependency(name="vein_get_id", depends=["vein_create"])
    async def test_get_vein(self, client: AsyncClient, gen_vein: VeinShort):
        response = await client.get(
            '/get_vein',
            params={
                'vein_id': TestMineral.stored_data['vein_id']
            }
        )
        assert response.status_code == 200, response.text
        assert response.json()['slug'] == gen_vein.slug

    @mark.dependency(name="vein_get_slug", depends=["vein_create"])
    async def test_get_vein_slug(self, client: AsyncClient, gen_vein: VeinShort):
        response = await client.get(
            '/get_vein',
            params={
                'vein_slug': gen_vein.slug
            }
        )
        assert response.status_code == 200, response.text
        assert response.json()['id'] == TestMineral.stored_data['vein_id']
        assert response.json()['slug'] == gen_vein.slug

    @mark.dependency(name="source_create", depends=["vein_create"])
    async def test_create_source(self, client: AsyncClient, gen_source: SourceShort):
        gen_source.vein_id = TestMineral.stored_data['vein_id']
        gen_source.source_metadata = {'some_data': 'some_data'}
        response = await client.post(
            '/add_source',
            json=gen_source.model_dump()
        )
        assert response.status_code == 200, "Not success response"
        assert response.json()['created_id']
        TestMineral.stored_data['source_id'] = response.json()['created_id']

    @mark.dependency(name="source_get_id", depends=["source_create"])
    async def test_get_source(self, client: AsyncClient, gen_source: SourceShort):
        loguru.logger.debug(TestMineral.stored_data['source_id'])
        response = await client.get(
            '/get_source',
            params={
                'source_id': TestMineral.stored_data['source_id']
            }
        )
        assert response.status_code == 200
        assert gen_source.slug == response.json()['slug']
        assert gen_source.vein_id == response.json()['vein_id']

    @mark.dependency(name="source_get_slug", depends=["source_get_id"])
    async def test_get_source_by_slug(self, client: AsyncClient, gen_source: SourceShort):
        response = await client.get(
            '/get_source',
            params={
                'source_slug': gen_source.slug
            }
        )
        assert response.status_code == 200
        assert gen_source.vein_id == response.json()['vein_id']
        assert gen_source.slug == response.json()['slug']

    @mark.dependency(name="source_create", depends=["source_create"])
    async def test_create_mineral(self, client: AsyncClient, gen_mineral: MineralAndAttachmentsShort):
        response = await client.post(
            '/add_tag',
            json={
                'descriptor': uuid4().hex
            }
        )
        assert response.status_code == 200
        assert response.json()['created_id']
        tag_id = response.json()['created_id']
        gen_mineral.source_id = TestMineral.stored_data['source_id']
        loguru.logger.debug(gen_mineral)
        loguru.logger.debug(gen_mineral.model_dump())
        adapter = TypeAdapter(list[MineralAndAttachmentsShort])
        gen_mineral.tags = [tag_id]
        response = await client.post(
            '/new_minerals',
            json={
                'serialization_type': 'json',
                'binary_minerals': b64encode(
                    adapter.dump_json([gen_mineral])
                ).decode()
            }
        )
        assert response.status_code == 200, "Not success response"
