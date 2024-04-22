from asyncio import gather
from iu_carrige.database.redis.core import Redis
from redis.asyncio import Redis
from itertools import cycle


HASHES_NAME = 'hashes'


class RedisHelper:
    def __init__(self, client: Redis):
        self.client = client

    async def push_hash(self, _hash: str):
        await self.client.hset(HASHES_NAME, _hash, '0')

    async def push_bulk_hash(self, hashes: list[str]):
        await self.client.hset(
            HASHES_NAME, mapping=dict(
                zip(
                    hashes,
                    cycle('0')
                )
            )
        )

    async def check_hash(self, _hash: str) -> bool:
        return await self.client.hexists(HASHES_NAME, _hash)
    
    async def check_bulk_hash(self, hashes: list[str]) -> tuple[bool]:
        return await gather(
            *(self.check_hash(_hash) for _hash in hashes)
        )


__all__ = [
    'RedisHelper'
]