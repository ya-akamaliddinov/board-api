from enum import Enum

from fastapi import APIRouter

router = APIRouter(prefix="/posts")


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get("/")
async def get_post():
    return {"status": "ok"}

@router.post("/")
async def create_post():
    ...

@router.put("/")
async def update_post():
    ...

@router.delete("/")
async def delete_post():
    ...
