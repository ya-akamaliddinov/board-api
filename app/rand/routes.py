# GET Query rnd_from and rnd_to returns random int in this diaposon
from random import randrange

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/random")


@router.get("/")
async def get_random(rnd_from: int = 0, rnd_to: int = 100):
    if rnd_from > rnd_to:
        raise HTTPException(status_code=400, detail="rnd_from должен быть > rnd_to")
    return {"num": randrange(rnd_from, rnd_to)}
