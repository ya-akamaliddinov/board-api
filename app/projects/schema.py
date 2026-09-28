from pydantic import BaseModel


class ProjectGetRequest(BaseModel):
    content: str


class ProjectCreateRequest(BaseModel):
    content: str


class ProjectUpdateRequest(BaseModel):
    content: str


class ProjectDeleteRequest(BaseModel):
    content: str
