from pydantic import field_validator

from .base_conf import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    DATABASE_URL: str = ""
    CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://127.0.0.1",
    ]
    SENTRY_DSN: str = ""
    BASE_URL: str = ""
    POOL_PRE_PING: bool = True
    POOL_RECYCLE: int = 3600
    ECHO: bool = False

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def validate_db_url(cls, db_url: str, driver: str = "psycopg2"):
        if db_url.startswith("postgres://"):
            return db_url.replace("postgres://", "postgresql://", 1)
        if db_url.startswith("postgresql://"):
            return db_url.replace("postgresql://", f"postgresql+{driver}://", 1)
        return db_url
