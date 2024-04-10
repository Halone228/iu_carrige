from .core import app
from .routes import core_router, cache_router, tags_router, source_router, vein_router
import iu_carrige.subs

app.include_router(core_router)
app.include_router(cache_router)
app.include_router(tags_router)
app.include_router(source_router)
app.include_router(vein_router)
