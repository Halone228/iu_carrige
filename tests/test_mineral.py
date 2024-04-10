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

    @mark.dependency(name="source_create", depends=["vein_create"])
    async def test_create_source(self, client: AsyncClient, gen_source: SourceShort):
        gen_source.vein_id = TestMineral.stored_data['vein_id']
        gen_source.metadata = {'some_data': 'some_data'}
        response = await client.post(
            '/add_source',
            json=gen_source.model_dump()
        )
        assert response.status_code == 200, "Not success response"
        assert response.json()['created_id']
        TestMineral.stored_data['source_id'] = response.json()['created_id']

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
