from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    email: str
    password: str

    model_config = {"extra": "forbid"}

class UserLoginRequest(BaseModel):
    email: str
    password: str

    model_config = {"extra": "forbid"}

class JWTResponce(BaseModel):
    token: str
