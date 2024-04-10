from typing import TypeVar, Type
from iu_carrige.database.sql import BaseDatabaseDep, asessionmaker
from iu_carrige.database.redis import RedisHelper, redis_client
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

dep_type = TypeVar('dep_type', bound=Type[BaseDatabaseDep])


async def get_session():
	async with asessionmaker() as session:
		yield session


def sql_helper_factory(_dep: Type[dep_type]):
	async def dep(session: Annotated[AsyncSession, Depends(get_session)] = None) -> dep_type:
		if session is None:
			async with asessionmaker() as session:
				instance = _dep(session)
				yield instance
		else:
			instance = _dep(session)
			yield instance
	return dep


async def get_redis_helper():
	async with redis_client as client:
		yield RedisHelper(client=client)


__all__ = [
	'sql_helper_factory',
	'get_redis_helper',
	'RedisHelper'
]
