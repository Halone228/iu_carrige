from loguru import logger

from iu_carrige.database.sql.models import *  # noqa
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC
from sqlalchemy import select, update, Executable, util  # noqa
from sqlalchemy.dialects.postgresql import insert  # noqa
from types import FunctionType


class BaseDatabaseDep(ABC):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def close(self):
        await self.session.close()


def async_raise_none(func: FunctionType):
    """In any case, when exception raised return `None`"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            return None
    wrapper.__annotations__ = func.__annotations__
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

