from .include import *
from iu_datamodels import TagShort, Tag as TagFull
from aiocache import cached
from pydantic import TypeAdapter


class TagDep(BaseDatabaseDep):
	async def create_tag(self, tag: TagShort) -> int:
		stmt = insert(Tag).values(descriptor=tag.descriptor).returning(
			Tag.id
		)
		try:
			_id = (await self.session.execute(stmt)).scalar()
		except IntegrityError:
			return -1
		await self.session.commit()
		return _id

	@async_raise_none
	async def get_tags(
		self,
		page: int = 1,
		limit: int = 100,
		query: str = None
	) -> list[TagFull]:
		stmt = select(Tag).limit(limit).offset((page - 1) * limit)
		if query is not None:
			stmt.where(
				Tag.descriptor.ilike(f'%{query}%')
			)
		result = await self.session.stream_scalars(stmt)
		return [
			TagFull.model_validate(i, from_attributes=True) async for i in result
		]

	@cached(
		noself=True
	)
	@async_raise_none
	async def get_tag_by(self, _id: int) -> TagFull:
		stmt = select(Tag).where(Tag.id == _id)
		data = await self.session.execute(stmt)
		return TagFull.model_validate(data.scalar(), from_attributes=True)

	async def get_bulk_tag(self, ids: list[int]) -> list[TagFull]:
		stmt = select(Tag).where(
			Tag.id.in_(ids)
		)
		data = await self.session.execute(stmt)
		return [
			TagFull.model_validate(i, from_attributes=True) for i in data.scalars()
		]

	async def get_all_tags(self) -> list[TagFull]:
		result = await self.session.execute(select(Tag))
		return TypeAdapter(list[TagFull]).validate_python(result.scalars())


__all__ = [
	'TagDep'
]