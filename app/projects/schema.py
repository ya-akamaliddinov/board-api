from pydantic import BaseModel, Field


class ProjectRequest(BaseModel):
    content: str = Field(min_length=1)
