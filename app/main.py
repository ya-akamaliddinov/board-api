from fastapi import FastAPI
from projects.routes import router as projects_router

app = FastAPI(
    title="BoardAPI",
    description="API для работы приложения",
    version="0.0.1",
    openapi_tags=[({"name": "Projects", "description": "Управление проектами."})],
)

app.include_router(projects_router)
