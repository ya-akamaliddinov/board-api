from typing import Annotated

from fastapi import Depends, HTTPException

from app.projects.model import Post
from app.projects.repository import PostRepository, PostRepositoryDeps
from app.projects.schema import PostCreateRequest, PostSearchParams, PostUpdateRequest


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def read(self, post_id: int):
        post = await self.repo.get_post_by_id(post_id)
        if post is None:
            raise HTTPException(
                status_code=404, detail="Post not found or was deleted."
            )

        return post

    async def list(self, params: PostSearchParams):
        return await self.repo.search(offset=params.offset, limit=params.limit)

    async def create(self, data: PostCreateRequest):
        post = Post(content=data.content)
        return await self.repo.save(post)

    async def update(self, post_id: int, data: PostUpdateRequest):
        post = await self.repo.get_post_by_id(post_id)
        if post is None:
            raise HTTPException(
                status_code=404, detail="Post not found or was deleted."
            )

        patch = data.model_dump(exclude_unset=True)
        for field, value in patch.items():
            setattr(post, field, value)

        return await self.repo.save(post)

    async def like(self, post_id: int):
        post = await self.repo.get_post_by_id(post_id)
        if post is None:
            raise HTTPException(
                status_code=404, detail="Post not found or was deleted."
            )

        return await self.repo.update_like(post)

    async def delete(self, post_id: int):
        post = await self.repo.get_post_by_id(post_id)
        if post is None:
            raise HTTPException(
                status_code=404, detail="Post not found or was deleted."
            )

        await self.repo.delete(post)


def get_post_service(repo: PostRepositoryDeps):
    return PostService(repo)


PostServiceDeps = Annotated[PostService, Depends(get_post_service)]
