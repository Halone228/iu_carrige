from httpx import AsyncClient
from uuid import uuid4
from loguru import logger
from pytest import mark


class TestHash:

    @mark.dependency(name="cache_push")
    async def test_push_hash(self, client: AsyncClient, hash_data):
        logger.info(f'Pushing {hash_data} to cache')
        response = await client.post(
            '/push_hashes', json=[
                hash_data
            ]
        )
        assert response.status_code == 200, 'Server error'
        assert response.json()['success']
        logger.info('Pushing success')

    @mark.dependency(name="check_cache", depends=["cache_push"])
    async def test_check_hash(self, client: AsyncClient, hash_data):
        logger.info(f'Checking {hash_data}')
        response = await client.get(
            '/check_hashes',
            params={
                'hashes': [hash_data, 'random_data']
            }
        )
        logger.info(f'Get response {repr(response.json())} from {[hash_data, "random_data"]}')
        assert response.json()[0]
        assert not response.json()[1]

