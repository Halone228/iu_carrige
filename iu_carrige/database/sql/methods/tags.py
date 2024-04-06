from .include import *
from iu_datamodels import TagShort


class TagDep(BaseDatabaseDep):
	async def create_tag(self, tag: TagShort) -> int:
		stmt = insert(Tag).values(descriptor=tag.descriptor).returning(
			Tag.id
		)
		return (await self.session.execute(stmt)).scalar()
