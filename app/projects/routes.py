from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Body, Path

from .schema import ProjectCreateRequest, ProjectResponse, ProjectUpdateRequest

router = APIRouter(prefix="/v1/projects", tags=["Projects"])


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get(
    "/{post_id}",
    response_model=ProjectResponse,
    description="""Получает проект по его ID""",
)
async def get_post(post_id: Annotated[int, Path(ge=1)]):
    return ProjectResponse(post_id=post_id, content="smth")


@router.post(
    "/", response_model=ProjectResponse, description=""""Создают новый проект"""
)
async def create_post(data: Annotated[ProjectCreateRequest, Body()]):
    return ProjectResponse(post_id=1, content=data.content)


@router.put(
    "/{post_id}",
    response_model=ProjectResponse,
    description=""""Обновляет проект по его ID""",
)
async def update_post(
    post_id: Annotated[int, Path(ge=1)], data: Annotated[ProjectUpdateRequest, Body()]
):
    return ProjectResponse(post_id=post_id, content=data.content)


@router.delete("/{post_id}", description="""Удаляет проект по его ID""")
async def delete_post(post_id: Annotated[int, Path(ge=1)]): ...
