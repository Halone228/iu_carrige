from .include import *
from iu_datamodels import SourceShort, Source


source_router = APIRouter(
    tags=['Source']
)


@source_router.post(
    '/add_source',
    response_model=CreatedModel
)
async def create_source(
    source_db: Annotated[SourceDep, Depends(sql_helper_factory(SourceDep))],
    source_data: SourceShort
):
    created_id = await source_db.create_source(source_data)
    return {
        'created_id': created_id
    }


@source_router.get(
    '/get_source',
    response_model=Source | None
)
async def get_source(
    source_db: Annotated[SourceDep, Depends(sql_helper_factory(SourceDep))],
    source_id: Annotated[int, Query()] = None,
    source_slug: Annotated[str, Query()] = None
):
    if not any((source_slug, source_id)) or all((source_slug, source_id)):
        raise HTTPException(
            status_code=422,
            detail="Only one of source_id or source_slug can be provided"
        )
    if source_slug:
        return await source_db.get_source_by_slug(source_slug)
    return await source_db.get_source(source_id)


