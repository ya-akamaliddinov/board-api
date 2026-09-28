from enum import Enum

from fastapi import APIRouter

router = APIRouter(prefix="/posts")


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get("/")
async def get_post():
    return {"status": "ok"}

@router.post("/{post_id}")
async def create_post(post_id: int):
    ...

@router.put("/{post_id}")
async def update_post(post_id: int):
    ...

@router.delete("/{post_id}")
async def delete_post(post_id):
    ...
