from .core import app
from .routes import core_route, cache_router

app.include_router(core_route)
app.include_router(cache_router)
