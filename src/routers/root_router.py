from fastapi import APIRouter

from src.logging import get_logging

logger = get_logging(__name__)

root_router = APIRouter(prefix="/api", tags=["root"])


@root_router.get("/")
async def root():
    return {"message": "Hello World"}


@root_router.get("/health")
async def get_health():
    return True


@root_router.get("/ping")
async def get_pong():
    logger.info('Кто то запросил "ping"')
    return "pong"


@root_router.get("/sentry-debug")
async def trigger_error():
    1 / 0
