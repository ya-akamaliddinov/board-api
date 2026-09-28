from fastapi import FastAPI
from projects.routes import router as projects_router

app = FastAPI()

app.include_router(projects_router)
