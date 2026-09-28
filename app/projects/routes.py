from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Body, Path

from .schema import ProjectCreateRequest, ProjectRequest

router = APIRouter(prefix="/projects")


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get("/{post_id}")
async def get_post(post_id: Annotated[ProjectRequest, Path(ge=1)]):
    return {"status": "ok"}


@router.post("/")
async def create_post(data: Annotated[ProjectCreateRequest, Body()]): ...


@router.put("/{post_id}")
async def update_post(
    post_id: Annotated[ProjectRequest, Path(ge=1)],
    data: Annotated[ProjectCreateRequest, Body()]
    ): ...


@router.delete("/{post_id}")
async def delete_post(
    post_id: Annotated[ProjectRequest, Path(ge=1)]
    ): ...
