from iu_carrige.database.models import *  # noqa
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from sqlalchemy import select, update, Executable, util  # noqa
from sqlalchemy.dialects.postgresql import insert  # noqa
from functools import wraps


class BaseDatabaseDep(ABC):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def close(self):
        await self.session.close()
