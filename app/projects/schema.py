from pydantic import BaseModel, Field


class ProjectRequest(BaseModel):
    post_id: int


class ProjectCreateRequest(BaseModel):
    content: str = Field(min_length=1)
