from .include import *
from iu_datamodels import VeinShort, Vein as VeinDataModel


vein_router = APIRouter(
    tags=['Vein']
)


@vein_router.post(
    '/add_vein',
    response_model=CreatedModel
)
async def create_vein(
    vein: VeinShort,
    vein_db: Annotated[VeinDep, Depends(sql_helper_factory(VeinDep))]
):
    created_id = await vein_db.create_vein(vein)
    return {
        'created_id': created_id
    }


@vein_router.get(
    '/search_vein',
    response_model=list[VeinDataModel]
)
async def search_vein(
    vein_db: Annotated[VeinDep, Depends(sql_helper_factory(VeinDep))],
    query: Annotated[str, Query()] = ''
):
    data = await vein_db.search_veins(query)
    return data


@vein_router.get(
    '/get_vein',
    description="Get a vein by its ID or slug(only one parameter must be provided)",
)
async def get_vein(
    vein_db: Annotated[VeinDep, Depends(sql_helper_factory(VeinDep))],
    vein_id: Annotated[int, Query()] = None,
    vein_slug: Annotated[str, Query()] = None,
):
    if not any((vein_id, vein_slug)):
        raise HTTPException(
            status_code=422,
            detail='One of vein_id, slug must be provided'
        )
    if all((vein_id, vein_slug)):
        raise HTTPException(
            status_code=422,
            detail="Only one of vein_id, slug must be provided"
        )
    if vein_id:
        v = await vein_db.get_vein(vein_id)
    else:
        v = await vein_db.get_vein_by_slug(vein_slug)
    return v
