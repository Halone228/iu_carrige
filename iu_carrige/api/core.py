from fastapi import FastAPI
from pkgutil import iter_modules
from . import routes
from fastapi import APIRouter


app = FastAPI()


for mod, name, _ in iter_modules([routes.__file__]):
    package = getattr(routes, name, None)
    if package is None or getattr(package, '__all__', None) is None:
        continue
    for export_name in getattr(package, '__all__'):
        if isinstance((export_item := getattr(package, export_name)), APIRouter):
            app.include_router(export_item)