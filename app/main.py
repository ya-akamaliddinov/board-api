from fastapi import FastAPI
from posts.routes import router as post_router
from rand.routes import router as rand_router

app = FastAPI()

app.include_router(post_router)
app.include_router(rand_router)
