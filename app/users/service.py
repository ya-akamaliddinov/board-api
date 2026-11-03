from typing import Annotated

from fastapi import HTTPException, Depends

from app.users.repository import UserRepositoryDeps
from app.users.schema import UserRegisterRequest, UserLoginRequest
from app.users.security import hash_password, verify_password
from app.users.model import User
from app.users.jwt import create_access_token


class UserService:
    def __init__(self, repo: UserRepositoryDeps):
        self.repo = repo

    async def get(self, user_id: int):
        user = await self.repo.get_by_id(user_id)
        return user

    async def create(self, data: UserRegisterRequest):
        user = await self.repo.get_by_email(data.email)
        if user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed = hash_password(data.password)
        user = User(name=data.name, email=data.email, password_hash=hashed)
        saved_user = await self.repo.create(user)
        return create_access_token(saved_user.id)

    async def authenticate(self, data: UserLoginRequest):
        user = await self.repo.get_by_email(data.email)

        if user is None:
            return None
        if not verify_password(data.password, user.password_hash):
            return None

        return create_access_token(user_id=user.id)

def get_user_service(repo: UserRepositoryDeps):
    return UserService(repo)


UserServiceDeps = Annotated[UserService, Depends(get_user_service)]
