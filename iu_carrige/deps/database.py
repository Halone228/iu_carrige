from typing import TypeVar, Type
from iu_carrige.database.sql import BaseDatabaseDep, asessionmaker
from iu_carrige.database.redis import RedisHelper, redis_client
from typing import AsyncIterator

dep_type = TypeVar('dep_type', bound=Type[BaseDatabaseDep])


def sql_helper_factory(_dep: Type[dep_type]):
	async def dep() -> dep_type:
		async with asessionmaker() as session:
			instance = dep_type(session)
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
