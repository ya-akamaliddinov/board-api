from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    name: str
    email: str
    password: str

    model_config = {"extra": "forbid"}

class UserLoginRequest(BaseModel):
    email: str
    password: str

    model_config = {"extra": "forbid"}

class JWTResponce(BaseModel):
    token: str
