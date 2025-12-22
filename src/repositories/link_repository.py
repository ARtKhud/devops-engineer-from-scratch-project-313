from typing import Optional, Sequence

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db
from src.models import Link
from src.schemas import LinkCreate
from src.schemas.link_schemas import LinkUpdate

BASE_URL = settings.BASE_URL


class LinkRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> Sequence[Link]:
        stmt = select(Link).order_by(Link.id)
        links = self.session.execute(stmt).scalars().all()
        return links

    def create_link(self, link: LinkCreate) -> Link:
        short_url = f"{BASE_URL}/r/{link.short_name}"
        created_link = Link(
            **link.model_dump(),
            short_url=short_url,
        )
        self.session.add(created_link)
        self.session.commit()
        self.session.refresh(created_link)
        return created_link

    def find_link_by_id(self, id: int) -> Optional[Link]:
        stmt = select(Link).where(Link.id == id)
        link = self.session.execute(stmt).scalar_one_or_none()
        return link

    def find_by_short_name(self, short_name: str) -> Optional[Link]:
        stmt = select(Link).where(Link.short_name == short_name)
        link = self.session.execute(stmt).scalar_one_or_none()
        return link

    def update_link(self, id: int, link_updates: LinkUpdate) -> Optional[Link]:
        upadeting_link = self.find_link_by_id(id)
        if not upadeting_link:
            return None
        for key, value in link_updates.model_dump().items():
            setattr(upadeting_link, key, value)
        self.session.add(upadeting_link)
        self.session.commit()
        self.session.refresh(upadeting_link)
        return upadeting_link

    def delete_link(self, id: int) -> None:
        stmt = select(Link).where(Link.id == id)
        link = self.session.execute(stmt).scalar_one()
        self.session.delete(link)
        self.session.commit()

    def get_total(self) -> int:
        stmt = select(func.count(Link.id))
        count = self.session.execute(stmt).scalar_one()
        return count


def get_link_repository(session: Session = Depends(get_db)) -> LinkRepository:
    return LinkRepository(session)
