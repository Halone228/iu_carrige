from iu_carrige.deps import sql_helper_factory
from iu_carrige.database.sql import MineralDep
from iu_carrige.events import new_mineral_event
from contextlib import asynccontextmanager
from iu_datamodels import MineralAndAttachments


async def process_new_mineral(minerals: list[MineralAndAttachments]):
	async with asynccontextmanager(sql_helper_factory(MineralDep)) as helper:
		helper: MineralDep
		await helper.new_mineral_bulk(minerals)

new_mineral_event.connect(process_new_mineral)
