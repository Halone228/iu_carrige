from .include import *
from iu_datamodels import MineralAndAttachmentsShort
from loguru import logger


class MineralDep(BaseDatabaseDep):
    async def close(self):
        await self.session.close()

    async def new_mineral_bulk(self, minerals: list[MineralAndAttachmentsShort]):
        stmt = insert(Mineral).returning(Mineral.id)
        result = await self.session.execute(
            stmt, tuple({
                'source_id': mineral.source_id,
                'html_text': mineral.html_text,
                'created_at': mineral.created_at
            } for mineral in minerals)
        )
        await self.session.commit()

        logger.debug(minerals)

        minerals = tuple(zip(minerals, result.scalars()))
        data_attachments = list(
            chain(
                *(({'mineral_id': mineral_id, 'attachment_id': a_id} for a_id in mineral.attachments)
                  for mineral, mineral_id in minerals)
            )
        )
        data_tags = list(
            chain(
                *(({'mineral_id': mineral_id, 'tag_id': t_id} for t_id in mineral.tags)
                  for mineral, mineral_id in minerals)
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
        await self.session.commit()


__all__ = [
    'MineralDep'
]