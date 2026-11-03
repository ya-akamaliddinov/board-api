from __future__ import annotations


from datetime import datetime

from pydantic import BaseModel, Field




# 1. Урезанная схема для дочерних ответов (без рекурсии, не вызовет MissingGreenlet)
class PostSimpleResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime | None
    likes_count: int
    parent_id: int | None
    is_deleted: bool

    class Config:
        from_attributes = True


# 2. Главная схема для корневого поста (у нее replies ссылается на PostSimpleResponse)
class PostResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime | None
    likes_count: int
    parent_id: int | None
    is_deleted: bool
    # Используем простую схему, поэтому Pydantic не полезет глубже в базу за ответами ответов
    replies: list[PostSimpleResponse] | None = None

    class Config:
        from_attributes = True


class PostCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=280)


class PostUpdateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=280)


class PostReplyRequest(PostCreateRequest):
    parent_id: int


class PostSearchParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=1000)


class PostSearchResponce(BaseModel):
    items: list[PostResponse]
    offset: int
    limit: int
