from .include import *
from iu_datamodels import MineralAndAttachmentsShort, MineralAndAttachments
from loguru import logger
from pydantic import TypeAdapter


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

    async def get_mineral(self, mineral_id: int) -> MineralAndAttachments:
        stmt = select(Mineral).where(Mineral.id == mineral_id)
        result = await self.session.execute(stmt)
        return TypeAdapter(MineralAndAttachments).validate_python(result.scalar(), from_attributes=True)

    async def get_mineral_bulk(self, mineral_ids: list[int]) -> list[MineralAndAttachments]:
        stmt = select(Mineral)
        result = await self.session.execute(
            stmt,
            [{'id': i} for i in mineral_ids]
        )
        return TypeAdapter(list[MineralAndAttachments]).validate_python(result.scalars(), from_attributes=True)

    async def get_minerals_by_tag(self, tags: list[int]) -> list[int]:
        stmt = select(MineralTag.mineral_id).where(
            MineralTag.tag_id.in_(tags)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars()) # noqa

    async def get_all_minerals(self) -> list[MineralAndAttachments]:
        stmt = select(Mineral)
        result = await self.session.execute(stmt)
        return TypeAdapter(list[MineralAndAttachments]).validate_python(result.scalars(), from_attributes=True)


__all__ = [
    'MineralDep'
]