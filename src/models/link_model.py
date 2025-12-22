from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base_model import Base


class Link(Base):
    original_url: Mapped[str] = mapped_column(String(100))
    short_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )
    short_url: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
    )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id},"
            f" title={self.original_url},"
            f" author_id={self.short_name})"
        )

    def __repr__(self) -> str:
        return str(self)
