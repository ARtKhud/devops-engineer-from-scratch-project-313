import logging
import os

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



SENTRY_DSN = os.getenv('SENTRY_DSN')

sentry_sdk.init(dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    send_default_pii=True,)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]
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