from asyncio import gather
from .include import *
from iu_carrige.utils import deserialize
from base64 import b64decode
from iu_datamodels import MineralAndSource
from iu_carrige.events import new_mineral_event

core_route = APIRouter(
    tags=['Minerals', 'Attachments']
)
        

@core_route.post('/new_minerals')
async def new_minerals(
    serelization_type: Annotated[str, Body()],
    binary_minerals: Annotated[str, Body()]
): 
    binary = b64decode(binary_minerals)
    data = deserialize(serelization_type, binary)
    await gather(
        *(
            new_mineral_event.send_async(MineralAndSource.model_validate(i, from_attributes=True)) for i in data
        )
    )


__all__ = [
    'core_route'
]