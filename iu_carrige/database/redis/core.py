from redis.asyncio import Redis
from os import getenv


redis_client = Redis.from_url(getenv("REDIS_CONNECT_URL"))


__all__ = [
    'redis_client'
]