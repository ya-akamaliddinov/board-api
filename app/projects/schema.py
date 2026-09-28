from pydantic import BaseModel, Field


class ProjectRequest(BaseModel):
    id: int


class ProjectCreateRequest(BaseModel):
    content: str = Field(min_length=1)


class ProjectUpdateRequest(BaseModel):
    content: str = Field(min_length=1)
