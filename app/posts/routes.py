from enum import Enum

from fastapi import APIRouter, Body

router = APIRouter(prefix="/posts")


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get("/{post_id}")
async def get_post(post_id: int):
    return {"status": "ok"}


@router.post("/")
async def create_post(post_id: int = Body()): ...


@router.put("/{post_id}")
async def update_post(post_id: int): ...


@router.delete("/{post_id}")
async def delete_post(post_id: int): ...
