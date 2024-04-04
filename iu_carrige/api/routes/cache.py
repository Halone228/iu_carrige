from .include import *
from iu_carrige.deps import get_redis_helper, RedisHelper
from loguru import logger

cache_router = APIRouter(
    tags=['Cache']
)


@cache_router.post('/push_hashes')
async def push_hashes(
    hashes: Annotated[list[str], Body()],
    redis_helper: Annotated[RedisHelper, Depends(get_redis_helper)]
):
    try:
        await redis_helper.push_bulk_hash(hashes)
    except Exception as e:
        logger.exception(e)
        return {
            'success': False
        }
    else:
        return {
            'success': True
        }


@cache_router.get('/check_hashes')
async def check_hashes(redis_helper: Annotated[RedisHelper, Depends(get_redis_helper)],
                       hashes: Annotated[list[str], Query()]) -> list[bool]:
    if hashes is None:
        raise HTTPException(
            status_code=400,
            detail='No hashes specified'
        )
    return list(await redis_helper.check_bulk_hash(hashes))
