from .include import *
from iu_datamodels import SourceShort


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

