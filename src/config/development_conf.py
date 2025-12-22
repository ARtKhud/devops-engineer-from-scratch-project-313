from pydantic_settings import SettingsConfigDict
from src.config.base_conf import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/dev_db"
    CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://127.0.0.1",
    ]
    SENTRY_DSN: str
    BASE_URL: str
    model_config = SettingsConfigDict(
        env_file=".env",
    )
    POOL_PRE_PING: bool = True
    POOL_RECYCLE: int = 3600
    ECHO: bool = True
