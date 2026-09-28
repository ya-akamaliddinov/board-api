from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Body

from .schema import ProjectCreateRequest, ProjectRequest, ProjectUpdateRequest

router = APIRouter(prefix="/posts")


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get("/{post_id}")
async def get_post(path: ProjectRequest):
    return {"status": "ok"}


@router.post("/")
async def create_post(data: Annotated[ProjectCreateRequest, Body()]): ...


@router.put("/{post_id}")
async def update_post(data: Annotated[ProjectUpdateRequest, Body()]): ...


@router.delete("/{post_id}")
async def delete_post(path: ProjectRequest): ...
