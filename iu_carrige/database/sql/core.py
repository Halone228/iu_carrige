from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from os import getenv
from iu_carrige.database.sql import models
from blinker import signal
from loguru import logger


USER = getenv("POSTGRES_USER") or None
PASSWORD = getenv("POSTGRES_PASSWORD") or None
HOST = getenv("POSTGRES_HOST")
PORT = getenv("POSTGRES_PORT")
DB = getenv("POSTGRES_DB")

uri = f"{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

engine = create_async_engine(f"postgresql+psycopg_async://{uri}")
asessionmaker = async_sessionmaker(bind=engine)


async def init_database(data):
    async with engine.connect() as connection:
        await connection.run_sync(models.Base.metadata.create_all)
        logger.debug(
            "Created tables: " + (", ".join(i for i in models.Base.metadata.tables))
        )
        await connection.commit()


signal("startup").connect(init_database)
