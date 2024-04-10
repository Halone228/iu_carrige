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
