from iu_carrige.database.sql.models import *  # noqa
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC
from sqlalchemy import select, update, Executable, util  # noqa
from sqlalchemy.dialects.postgresql import insert  # noqa


class BaseDatabaseDep(ABC):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def close(self):
        await self.session.close()
