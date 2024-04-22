from .include import *
from iu_datamodels import VeinShort, Vein as VeinDataModel


class VeinDep(BaseDatabaseDep):
    async def create_vein(self, vein: VeinShort) -> int:
        stmt = insert(Vein).values(
            name=vein.name,
            url=vein.url,
            slug=vein.slug
        ).returning(Vein.id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def search_veins(self, query: str) -> list[VeinDataModel]:
        stmt = select(Vein).limit(10).where(
            Vein.name.ilike(f'%{query}%')
        )
        result = await self.session.stream_scalars(stmt)
        return [
            VeinDataModel.model_validate(i, from_attributes=True) async for i in result
        ]

    async def get_vein(self, vein_id) -> VeinDataModel:
        stmt = select(Vein).where(
            Vein.id == vein_id
        )
        result = await self.session.execute(stmt)
        return VeinDataModel.model_validate(result.scalar(), from_attributes=True)

    @async_raise_none
    async def get_vein_by_slug(self, vein_slug: str) -> VeinDataModel:
        stmt = select(Vein).where(
            Vein.slug == vein_slug
        )
        result = await self.session.execute(stmt)
        return VeinDataModel.model_validate(result.scalar(), from_attributes=True)



__all__ = [
    'VeinDep'
]