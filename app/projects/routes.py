from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Body, Path

from .schema import ProjectCreateRequest, ProjectResponse, ProjectUpdateRequest
from .service import ProjectServiceDeps

router = APIRouter(prefix="/v1/projects", tags=["Projects"])


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get(
    "/{post_id}",
    response_model=ProjectResponse,
    status_code=200,
    summary="Получить проект по ID",
    description="""Получает проект по ID""",
)
async def get_post(servise: ProjectServiceDeps, post_id: Annotated[int, Path(ge=1)]):
    res = servise.get(post_id)
    return ProjectResponse(post_id=res, content="smth")


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=201,
    summary="Создать новый проект",
    description=""""Создают новый проект""",
)
async def create_post(data: Annotated[ProjectCreateRequest, Body()]):
    return ProjectResponse(post_id=1, content=data.content)


@router.put(
    "/{post_id}",
    response_model=ProjectResponse,
    status_code=200,
    summary="Обновить проект по ID",
    description=""""Обновляет проект по ID""",
)
async def update_post(
    post_id: Annotated[int, Path(ge=1)], data: Annotated[ProjectUpdateRequest, Body()]
):
    return ProjectResponse(post_id=post_id, content=data.content)


@router.delete(
    "/{post_id}",
    response_model=None,
    status_code=204,
    summary="Удалить проект по ID",
    description="""Удаляет проект по ID""",
)
async def delete_post(post_id: Annotated[int, Path(ge=1)]): ...
