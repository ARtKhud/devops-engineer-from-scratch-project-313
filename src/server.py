from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.config as config
from src.routers import link_router, root_router

from .database import db_init, dispose


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db_init()
    except Exception as e:
        print(f"Error during db_init: {e}")
        raise
    yield
    dispose()


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range"],
)

app.include_router(link_router)
app.include_router(root_router)
