import logging

from fastapi import APIRouter, HTTPException

from app.users.schema import UserRegisterRequest, JWTResponce, UserLoginRequest
from app.users.service import UserServiceDeps
from app.users.schema import UserResponce
from app.users.current_user import CurentUserDeps

router = APIRouter(prefix="/v1/users", tags=["Users"])

logger = logging.getLogger(__name__)



@router.get(
        "/me",
        response_model=UserResponce,
        status_code=200
)
async def get_me(
    current_user: CurentUserDeps
):
    return UserResponce(name=current_user.name, email=current_user.email)
    

@router.post(
    "/register",
    response_model=JWTResponce,
    status_code=201
)
async def register(
    data: UserRegisterRequest,
    service: UserServiceDeps
):
    token = await service.create(data)
    return JWTResponce(token=token)


@router.post(
    "/login",
    response_model=JWTResponce,
    status_code=200
)
async def login(
    data: UserLoginRequest,
    service: UserServiceDeps
):
    token = await service.authenticate(data)
    if token is None:
        raise HTTPException(status_code=401, detail="Wrong email or password.")
    return JWTResponce(token=token)