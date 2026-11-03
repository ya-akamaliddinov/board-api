from pydantic import BaseModel, Field


class UserRegisterRequest(BaseModel):
    name: str
    email: str
    password: str = Field(min_length=8, max_length=72)

    model_config = {"extra": "forbid"}


class UserLoginRequest(BaseModel):
    email: str
    password: str

    model_config = {"extra": "forbid"}


class UserResponce(BaseModel):
    name: str
    email: str


class JWTResponce(BaseModel):
    token: str
