from iu_carrige.database.redis import RedisHelper, redis_client


async def get_redis_helper():
    async with redis_client as client: 
        yield RedisHelper(client=client)


__all__ = [
    'get_redis_helper'
] 