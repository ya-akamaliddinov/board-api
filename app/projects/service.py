from typing import Annotated

from fastapi import Depends

from .repository import ProjectRepository, ProjectRepositoryDeps


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def get(self, post_id: int):
        return self.repo.get_project(post_id)


def get_project_service(repo: ProjectRepositoryDeps):
    return ProjectService(repo)


ProjectServiceDeps = Annotated[ProjectService, Depends(get_project_service)]
