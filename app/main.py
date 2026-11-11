from contextlib import asynccontextmanager

from fastapi import FastAPI

import models  # noqa: F401  (реєстрація моделей)
from api.v1.router import api_router
from core.config import settings
from core.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.AUTO_CREATE_TABLES:
        Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Shop API", version="1.0.0", lifespan=lifespan)
app.include_router(api_router)
