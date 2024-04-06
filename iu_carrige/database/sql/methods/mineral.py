from .include import *
from iu_datamodels import MineralAndAttachments


class MineralDep(BaseDatabaseDep):
    @override
    async def close(self):
        await self.session.close()

    async def new_mineral_bulk(self, minerals: list[MineralAndAttachments]):
        stmt = insert(Mineral).returning(Mineral.id)
        result = await self.session.execute(
            stmt, [mineral.model_dump() for mineral in minerals]
        )

        def apply(mineral_and_raw: tuple[MineralAndAttachments, int]):
            _mineral = mineral_and_raw[0]
            _mineral.id = mineral_and_raw[1]
            return _mineral

        minerals = tuple(map(apply, zip(minerals, result)))
        data_attachments = list(
            chain(
                *(({'mineral_id': mineral.id, 'attachment_id': a_id} for a_id in mineral.attachments)
                  for mineral in minerals)
            )
        )
        data_tags = list(
            chain(
                *(({'mineral_id': mineral.id, 'tag_id': t_id} for t_id in mineral.tags)
                  for mineral in minerals)
            )
        )
        coros = [
            self.session.execute(
                insert(MineralAttachment),
                data_attachments
            ),
            self.session.execute(
                insert(MineralTag),
                data_tags
            )
        ]
        await gather(*coros)


__all__ = [
    'MineralDep'
]