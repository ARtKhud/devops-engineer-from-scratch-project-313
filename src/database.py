from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.models.base_model import Base

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=settings.POOL_PRE_PING,
    pool_recycle=settings.POOL_RECYCLE,
    echo=settings.ECHO,
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def db_init():
    Base.metadata.create_all(bind=engine)


def dispose():
    engine.dispose()
