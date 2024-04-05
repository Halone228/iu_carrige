from .base import BaseDep
from aioboto3 import Session
from os import getenv
from contextlib import asynccontextmanager
from loguru import logger
from blinker import ANY
from iu_carrige.events import startup_event

AWS_DEFAULT_REGION = getenv("AWS_DEFAULT_REGION") or None
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY") or None
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID") or None
ENDPOINT_URL = getenv("AWS_ENDPOINT") or None
BUCKET_NAME = getenv("BUCKET_NAME") or "default"


@asynccontextmanager
async def file_storage_dep():
    session = Session()
    async with session.client(
        's3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    ) as s3_s:
        yield s3_s


async def init_s3(*args, **kwargs):
    async with file_storage_dep() as s3_s:
        try:
            await s3_s.create_bucket(Bucket=BUCKET_NAME)
        except Exception as e:
            logger.exception(e)

startup_event.connect(init_s3, ANY)

__all__ = [
    'file_storage_dep'
]