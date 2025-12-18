import logging
from contextlib import asynccontextmanager
from typing import List

import sentry_sdk
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

import config
from repositories.LinkRepository import LinkRepository

from .database import engine
from .models import LinkCreate, LinkResponse

sentry_sdk.init(dsn=config.SENTRY_DSN,
    traces_sample_rate=1.0,
    send_default_pii=True,)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        SQLModel.metadata.create_all(engine)
    except Exception:
        raise
    app.state.engine = engine
    yield 
    engine.dispose()


app = FastAPI(lifespan=lifespan)

repo = LinkRepository(engine)
origins = [
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range"]
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


@app.get("/api/links",
        response_model=List[LinkResponse],
        status_code=status.HTTP_200_OK)
async def get_links(response: Response, range: str = None):
    if range:
        start_str, end_str = range.strip("[]").split(",")
        skip = int(start_str.strip())
        limit = int(end_str.strip()) - skip + 1
        total_count = repo.get_total_count()
        links = repo.get_content(skip=skip, limit=limit)
        response.headers["Content-Range"] = (
            f"links {skip}-{limit + skip - 1}/{total_count}"
        ) 
        return links
    return repo.get_content()


@app.post("/api/links", status_code=status.HTTP_201_CREATED)
async def create_link(link_data: LinkCreate):
    link = repo._create(link_data.model_dump())
    return link


@app.get("/api/links/{id}")
async def get_link_by_id(id: int):
    link = repo.find(id)
    return link


@app.put("/api/links/{id}", status_code=status.HTTP_200_OK)
async def update_link(id: int, link_data: dict):
    link = repo._update(id, link_data)
    return link


@app.delete("/api/links/{id}")
async def delete_link(id: int):
    repo.delete(id)


@app.get("/health")
async def get_health():
    return True