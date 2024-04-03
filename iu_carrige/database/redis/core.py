from redis.asyncio import Redis
from os import getenv

url = getenv("REDIS_CONNECT_URL")
url = '' if not url else url
redis_client = Redis.from_url(url)


__all__ = [
    'redis_client'
]