from .include import *

core_route = APIRouter(
    tags=['Minerals', 'Attachments']
)


@core_route.get('/check_hashes')
async def check_hashes(redis_helper: Annotated[RedisHelper, Depends(get_redis_helper())], hashes: list[str] | None = None) -> list[bool]:
    if hashes is None:
        raise HTTPException(
            status_code=400,
            detail='No hashes specified'
        )
    return await redis_helper.check_bulk_hash(hashes) 
    
        

@core_route.post('/new_minerals')
async def new_minerals(): 
    pass


__all__ = [
    'core_route'
]