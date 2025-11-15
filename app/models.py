from datetime import datetime

from sqlmodel import Field, SQLModel


class Link(SQLModel, table=True):
    __tablename__ = "links"
    
    id: int | None = Field(default=None, primary_key=True)
    original_url: str
    short_name: str
    short_url: str
    created_at: datetime = Field(default_factory=datetime.now)
    

class LinkCreate(SQLModel):
    original_url: str
    short_name: str
