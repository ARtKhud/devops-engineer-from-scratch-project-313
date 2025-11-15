import logging
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

import config
from repositories.LinkRepository import LinkRepository

from .database import engine

sentry_sdk.init(dsn=config.SENTRY_DSN,
    traces_sample_rate=1.0,
    send_default_pii=True,)


print(config.os.getenv("DATABASE_URL"))
print(config.os.getenv("BASE_URL"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        raise
    app.state.engine = engine
    yield 
    engine.dispose()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8080",
]
repo = LinkRepository(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def get_pong():
    logger.info('Кто то запросил "ping"')
    return "pong"


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


@app.get("/api/links")
async def get_links():
    return repo.get_content()


@app.post("/api/links") 
async def create_link(link_data: dict):
    link = repo._create(link_data)
    return link


@app.get("/api/links/{id}")
async def get_link_by_id(id: int):
    link = repo.find(id)
    return link


@app.put("/api/links/{id}")
async def update_link(id: int, link_data: dict):
    link = repo._update(id, link_data)
    return link


@app.delete("/api/links/{id}")
async def delete_link(id: int):
    repo.delete(id)