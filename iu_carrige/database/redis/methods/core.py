from asyncio import gather
from iu_carrige.database.redis.core import Redis
from redis.asyncio import Redis


HASHES_NAME = 'hashes'


class RedisHelper:
    def __init__(self, client: Redis):
        self.client = client

    async def push_hash(self, hash: str):
        await self.client.hset(HASHES_NAME, hash, 0)

    async def push_bulk_hash(self, hashes: str):
        await gather(
            *(self.push_hash(hash) for hash in hashes)
        )

    async def check_hash(self, hash: str) -> bool:
       return await self.client.hexists(HASHES_NAME, hash) 
    
    async def check_bulk_hash(self, hashes: str) -> list[bool]:
        return await gather(
            *(self.check_hash(hash) for hash in hashes)
        )


__all__ = [
    'RedisHelper'
]