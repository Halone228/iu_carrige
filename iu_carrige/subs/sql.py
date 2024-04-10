from iu_carrige.database.sql import MineralDep
from iu_carrige.events import new_mineral_event
from iu_datamodels import MineralAndAttachmentsShort
from iu_carrige.database.sql.core import asessionmaker


async def process_new_mineral(minerals: list[MineralAndAttachmentsShort]):
	async with asessionmaker() as session:
		helper = MineralDep(session)
		await helper.new_mineral_bulk(minerals)

new_mineral_event.connect(process_new_mineral)
