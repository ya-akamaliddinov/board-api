from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.users.service import UserServiceDeps
from app.users.model import User
from app.users.jwt import decode_access_token

security = HTTPBearer()

async def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        service: UserServiceDeps
) -> User:
    token = credentials.credentials

    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await service.get(int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

CurentUserDeps = Annotated[User, Depends(get_current_user)]
