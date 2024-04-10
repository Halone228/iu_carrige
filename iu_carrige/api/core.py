from os import getenv

from fastapi import FastAPI
from iu_carrige.events import startup_event
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
	await startup_event.send_async()
	yield


app = FastAPI(
	lifespan=lifespan,
	debug=bool(getenv("DEBUG", None))
)
