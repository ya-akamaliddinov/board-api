import logging
from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path

from .schema import (
    PostCreateRequest,
    PostResponse,
    PostSearchParams,
    PostSearchResponce,
    PostUpdateRequest,
    PostReplyRequest,
    PostSimpleResponse
)
from .service import PostServiceDeps
from app.users.current_user import CurentUserDeps

router = APIRouter(prefix="/v1/posts", tags=["Posts"])

logger = logging.getLogger(__name__)


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get(
    "/",
    response_model=PostSearchResponce,
    status_code=200,
    summary="Поиск задач по параметрам.",
    description="""Поиск задач по параметрам offset, limit""",
)
async def search_post(
    servise: PostServiceDeps,
    params: PostSearchParams = Depends(),  # noqa: B008
    
):
    posts = await servise.list(params)
    return PostSearchResponce(
        items=[PostResponse.model_validate(t) for t in posts],
        offset=params.offset,
        limit=params.limit,
    )


@router.get(
    "/{post_id}",
    response_model=PostResponse,
    status_code=200,
    summary="Получить проект по ID",
    description="""Получает проект по ID""",
)
async def get_post(post_id: Annotated[int, Path(ge=1)], servise: PostServiceDeps):
    res, replies= await servise.read(post_id)
    logger.info("Get post by id=%s", post_id)
    return PostResponse(
        id=res.id,
        content=res.content,
        created_at=res.created_at,
        updated_at=res.updated_at,
        likes_count=res.likes_count,
        is_deleted=res.is_deleted,
        parent_id=res.parent_id,
        replies=replies
    )


@router.post(
    "/",
    response_model=PostSimpleResponse,
    status_code=201,
    summary="Создать новый проект",
    description=""""Создаёт новый проект""",
)
async def create_post(
    data: Annotated[PostCreateRequest, Body()],
    current_user: CurentUserDeps,
    service: PostServiceDeps
):
    res = await service.create(data, current_user.id)

    return PostSimpleResponse.model_validate(res)

@router.post(
        "/reply",
        response_model=PostResponse,
        status_code=200
)
async def reply(
    data: PostReplyRequest,
    current_user: CurentUserDeps,
    service: PostServiceDeps,
):
    res = await service.reply(data, current_user.id)
    return PostResponse.model_validate(res)
    

@router.put(
    "/{post_id}",
    response_model=PostResponse,
    status_code=200,
    summary="Обновить проект по ID",
    description=""""Обновляет проект по ID""",
)
async def update_post(
    post_id: Annotated[int, Path(ge=1)],
    data: Annotated[PostUpdateRequest, Body()],
    service: PostServiceDeps,
):
    res = await service.update(post_id, data)

    return PostResponse.model_validate(res)


@router.post(
    "/{post_id}/like",
    response_model=PostResponse,
    status_code=200,
    summary="Увеличить like поста",
    description="""Увеличить like поста по ID""",
)
async def update_like_post(
    post_id: Annotated[int, Path(ge=1)], 
    service: PostServiceDeps
):
    res = await service.like(post_id)

    return PostResponse.model_validate(res)


@router.delete(
    "/{post_id}",
    response_model=None,
    status_code=204,
    summary="Удалить проект по ID",
    description="""Удаляет проект по ID""",
)
async def delete_post(post_id: Annotated[int, Path(ge=1)], service: PostServiceDeps):

    await service.delete(post_id)
