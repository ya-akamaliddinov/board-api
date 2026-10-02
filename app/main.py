from fastapi import FastAPI

from app.core.settings import Settings
from app.projects.routes import router as projects_router


def create_app() -> FastAPI:
    settings = Settings()  # type: ignore[call-arg]
    new_app = FastAPI(
        title=settings.app.name,
        description="API для работы приложения",
        version=settings.app.version,
        openapi_tags=[({"name": "Projects", "description": "Управление проектами."})],
    )

    new_app.state.settings = settings

    new_app.include_router(projects_router)

    return new_app


app = create_app()
