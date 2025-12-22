from fastapi import APIRouter, Depends, Response, status

from src.schemas.link_schemas import LinkCreate, LinkUpdate
from src.services import LinkService, get_link_service

link_router = APIRouter(prefix="/api", tags=["links"])


@link_router.get("/links", status_code=status.HTTP_200_OK)
async def get_links(
    response: Response,
    range: str | None = None,
    service: LinkService = Depends(get_link_service),
):
    if not range:
        return service.get_all_links()
    start_str, end_str = map(int, range.strip("[]").split(","))
    print(start_str, end_str)
    skip, limit = start_str, end_str - start_str + 1
    total_count = service.get_total()
    response.headers["Content-Range"] = (
        f"links {skip}-{limit + skip - 1 }/{total_count}"
    )
    return service.get_all_links(skip, limit)


@link_router.post("/links", status_code=status.HTTP_201_CREATED)
async def create_link(
    link_creation_data: LinkCreate,
    service: LinkService = Depends(get_link_service),
):
    return service.create_link(link_creation_data)


@link_router.get("/links/{id}", status_code=status.HTTP_200_OK)
async def get_link_by_id(
    id: int, service: LinkService = Depends(get_link_service)
):
    link = service.get_link_by_id(id)
    return link


@link_router.put("/links/{id}", status_code=status.HTTP_200_OK)
async def update_link(
    id: int,
    link_updates: LinkUpdate,
    service: LinkService = Depends(get_link_service),
):
    link = service.update_link(id, link_updates)
    return link


@link_router.delete("/links/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(
    id: int, service: LinkService = Depends(get_link_service)
):
    service.delete_link(id)
