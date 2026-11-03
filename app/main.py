from fastapi import FastAPI

from app.core.settings import Settings
from app.projects.routes import router as projects_router
from app.users.routes import router as users_router


def create_app() -> FastAPI:
    settings = Settings()  # type: ignore[call-arg]
    new_app = FastAPI(
        title=settings.app.name,
        description="API для работы приложения",
        version=settings.app.version,
        openapi_tags=[
            ({"name": "Posts", "description": "Управление постами."}),
            ({"name": "Users", "description": "Управление пользователя."})
            
            ],
    )

    new_app.state.settings = settings

    new_app.include_router(projects_router)
    new_app.include_router(users_router)

    return new_app


app = create_app()
