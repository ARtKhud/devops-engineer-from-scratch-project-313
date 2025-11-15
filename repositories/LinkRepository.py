import os

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Link, LinkCreate

BASE_URL = os.getenv("BASE_URL")


class LinkRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with Session(self.conn) as session:
            links = session.exec(select(Link)).all()
            return links

    def find(self, id):
        with Session(self.conn) as session:
            link = session.get(Link, id)
            if not link:
                raise HTTPException(
                        status_code=404, 
                        detail="Not Found"
                    )
            return link

    def save(self, link_data):
        if "id" in link_data and link_data["id"]:
            self._update(link_data["id"], link_data)
        else:
            self._create(link_data)

    def _update(self, id: int, link_data: dict):
        with Session(self.conn) as session:
            link = session.get(Link, id)
            if not link:
                raise HTTPException(status_code=404, detail="Not Found")
            
            if link_data.get("short_name") != link.short_name:
                existing = self.find_by_short_name(link_data["short_name"])
                if existing and existing.id != id:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"'{link_data['short_name']}'already exists"
                    )
            
            for field, value in link_data.items():
                if hasattr(link, field):
                    setattr(link, field, value)
            
            if "short_name" in link_data:
                link.short_url = f"{BASE_URL}{link_data['short_name']}"
            
            session.add(link)
            session.commit()
            session.refresh(link)
            return link

    def _create(self, link_data: LinkCreate) -> Link:
        if self.find_by_short_name(link_data["short_name"]):
            raise HTTPException(
                status_code=400, 
                detail=f"Short name '{link_data['short_name']}' already exists"
            )
        
        with Session(self.conn) as session:
            link = Link(
                original_url=link_data["original_url"],
                short_name=link_data["short_name"],
                short_url=f"{BASE_URL}{link_data['short_name']}"
            )
            session.add(link)
            session.commit()
            session.refresh(link)
            return link
        
    def find_by_short_name(self, short_name: str):
        with Session(self.conn) as session:
            statement = select(Link).where(Link.short_name == short_name)
            link = session.exec(statement).first()
            return link
        
    def delete(self, id: int) -> bool:
        with Session(self.conn) as session:
            link = session.get(Link, id)
            if not link:
                raise HTTPException(status_code=404, detail="Link not found")
            session.delete(link)
            session.commit()
            raise HTTPException(status_code=204, detail="No Content")