from typing import Annotated

from fastapi import Depends


class ProjectRepository:
    def get_project(self, post_id: int):
        return post_id


def get_project_repository():
    return ProjectRepository()


ProjectRepositoryDeps = Annotated[ProjectRepository, Depends(get_project_repository)]
