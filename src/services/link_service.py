from typing import Optional

from fastapi import Depends, HTTPException, status

from src.repositories import LinkRepository
from src.repositories.link_repository import get_link_repository
from src.schemas import LinkCreate, LinkResponse
from src.schemas.link_schemas import LinkUpdate


class LinkService:
    def __init__(self, repo: LinkRepository):
        self.repo = repo

    def get_all_links(
        self, skip: int = 0, limit: int = 10
    ) -> list[LinkResponse]:
        links = self.repo.get_all()
        sliced_links = [LinkResponse.model_validate(link) for link in links][
            skip:limit:
        ]
        return sliced_links

    def create_link(self, lcd: LinkCreate) -> Optional[LinkResponse]:
        exsiting_link = self.repo.find_by_short_name(lcd.short_name)
        if not exsiting_link:
            link = self.repo.create_link(lcd)
            return LinkResponse.model_validate(link)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def get_link_by_id(self, id: int) -> LinkResponse:
        link = self.repo.find_link_by_id(id)
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return LinkResponse.model_validate(link)

    def update_link(self, id: int, link_updates: LinkUpdate) -> LinkResponse:
        link = self.repo.update_link(id, link_updates)
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return LinkResponse.model_validate(link)

    def get_total(self) -> int:
        return self.repo.get_total()

    def delete_link(self, id: int) -> None:
        self.get_link_by_id(id)
        self.repo.delete_link(id)


def get_link_service(
    repo: LinkRepository = Depends(get_link_repository),
) -> LinkService:
    return LinkService(repo)
