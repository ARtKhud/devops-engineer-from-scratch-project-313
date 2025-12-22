from typing import Optional
from pydantic import BaseModel, Field


class LinkBase(BaseModel):
    short_name: str = Field(
        ...,
        description="Short name",
        min_length=3,
        max_length=20,
    )


class LinkCreate(LinkBase):
    original_url: str = Field(
        ...,
        description="Original url",
        min_length=3,
        # max_length=10,
    )


class LinkUpdate(BaseModel):
    original_url: Optional[str] = Field(
        default=None,
        description="Original url",
        min_length=3,
        # max_length=10,
    )
    short_name: Optional[str] = Field(
        default=None,
        description="Short name",
        min_length=3,
        max_length=20,
    )


class LinkResponse(LinkUpdate):
    id: int = Field(..., description="Unique link indentifire")
    short_url: str = Field(..., description="Short url")

    class Config:
        from_attributes = True
