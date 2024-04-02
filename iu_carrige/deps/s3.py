from .base import BaseDep
from aioboto3 import Session
from os import getenv
from contextlib import asynccontextmanager


@asynccontextmanager
async def file_storage_dep():
    session = Session(
        region_name=getenv("S3_REGION")

    )
    async with session.resource('s3') as s3_s:
        yield s3_s