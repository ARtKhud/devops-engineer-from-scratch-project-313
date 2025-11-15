import os

from sqlalchemy import create_engine

from utils.add_driver import add_driver_to_db_url

DATABASE_URL = add_driver_to_db_url(os.getenv("DATABASE_URL"))

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

print(os.getenv("DATABASE_URL"))
print(os.getenv("BASE_URL"))

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=True
)