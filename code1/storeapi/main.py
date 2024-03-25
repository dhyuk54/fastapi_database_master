from contextlib import asynccontextmanager

from fastapi import FastAPI

from code1.storeapi.database import database
from code1.storeapi.routers.post import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


app.include_router(post_router)
