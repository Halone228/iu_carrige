from .base import BaseDep
from aioboto3 import Session
from os import getenv
from contextlib import asynccontextmanager


@asynccontextmanager
async def file_storage_dep():
    session = Session(
        region_name=getenv("S3_REGION"),
        aws_secret_access_key=getenv("S3_SECRET_ACCESS_KEY"),
        aws_access_key_id=getenv("S3_ACCESS_KEY")
    )
    async with session.resource('s3', endpoint_url=getenv("S3_URL")) as s3_s:
        yield s3_s
