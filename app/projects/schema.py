from datetime import datetime

from pydantic import BaseModel, Field


class PostResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime | None
    likes_count: int
    is_deleted: bool

    model_config = {"from_attributes": True}


class PostCreateRequest(BaseModel):
    content: str = Field(min_length=1)


class PostUpdateRequest(BaseModel):
    content: str | None = Field(default=None, min_length=1)


class PostSearchParams(BaseModel):
    offset: int = Field(0, ge=1)
    limit: int = Field(20, ge=1, le=1000)


class PostSearchResponce(BaseModel):
    items: list[PostResponse]
    offset: int
    limit: int
