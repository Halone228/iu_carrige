from .include import *
from iu_datamodels import SourceShort, Source as SourceDataModel


class SourceDep(BaseDatabaseDep):
    async def create_source(self, source: SourceShort) -> int:
        stmt = insert(Source).values(
            vein_id=source.vein_id,
            slug=source.slug,
            source_metadata=source.metadata
        ).returning(Source.id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def get_source(self, source_id: int) -> SourceDataModel:
        stmt = select(Source).where(
            Source.id == source_id
        )
        result = await self.session.execute(stmt)
        return SourceDataModel.model_validate(
            result.scalar()
        )


__all__ = [
    'SourceDep'
]