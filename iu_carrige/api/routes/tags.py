from iu_carrige.deps import sql_helper_factory
from iu_carrige.database.sql import TagDep
from .include import *
from iu_datamodels import TagShort, Tag


tags_router = APIRouter(
    tags=[
        'Tags'
    ]
)


@tags_router.post(
    '/add_tag',
    responses={
        400: {
            'description': 'Tag already exists',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Already exists'
                    }
                }
            }
        }
    },
    response_model=CreatedModel
)
async def create_tag(
    tag: TagShort,
    tag_db: Annotated[TagDep, Depends(sql_helper_factory(TagDep))]
):
    created_id = await tag_db.create_tag(tag)
    if created_id == -1:
        return {
            'detail': 'Already exists'
        }
    return {
        'created_id': created_id
    }


@tags_router .get(
    '/search_tags'
)
async def search_tags(
    tag_db: Annotated[TagDep, Depends(sql_helper_factory(TagDep))],
    page: int = 1,
    limit: int = 100,
    query: str = None
) -> list[Tag]:
    return await tag_db.get_tags(page, limit, query)
