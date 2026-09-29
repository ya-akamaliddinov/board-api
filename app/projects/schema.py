from pydantic import BaseModel, Field


class ProjectResponse(BaseModel):
    post_id: int
    content: str


class ProjectCreateRequest(BaseModel):
    content: str = Field(min_length=1)


class ProjectUpdateRequest(BaseModel):
    content: str | None = Field(default=None, min_length=1)
