from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status

from app.projects.model import Post
from app.projects.repository import PostRepository, PostRepositoryDeps
from app.projects.schema import (
    PostCreateRequest, PostSearchParams, PostUpdateRequest, PostReplyRequest
)

from app.core.settings import Settings

settings = Settings()  # type: ignore[call-arg]


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def read(self, post_id: int):
        post = await self.repo.get_post_by_id(post_id)
        if post is None or post.is_deleted:
            raise HTTPException(
                status_code=404, detail="Post not found or was deleted."
            )

        return post, post.replies

    async def list(self, params: PostSearchParams):
        return await self.repo.search(offset=params.offset, limit=params.limit)

    async def create(self, data: PostCreateRequest, author_id: int):
        # 1. Проверяем последний пост пользователя
        last_post = await self.repo.get_latest_post_by_author(author_id)
        
        if last_post and last_post.created_at:
            now = datetime.now(timezone.utc)
            last_post_time = last_post.created_at
            
            # Если база возвращает наивное время (без таймзоны), приводим к UTC
            if last_post_time.tzinfo is None:
                last_post_time = last_post_time.replace(tzinfo=timezone.utc)
                
            elapsed = now - last_post_time
            
            if elapsed < timedelta(seconds=settings.minimal_post_debounce_time):
                remaining = int(settings.minimal_post_debounce_time - elapsed.total_seconds())
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Слишком частые публикации. Подождите еще {remaining} сек."
                )

        # 2. Если всё ок, создаем пост (не забудьте про parent_id, если это ответ!)
        post = Post(
            content=data.content, 
            author_id=author_id,
            parent_id=getattr(data, "parent_id", None) # Если в PostCreateRequest есть parent_id
        )
        return await self.repo.save(post)

    async def reply(self, data: PostReplyRequest, author_id: int):
        post = await self.repo.get_post_by_id(data.parent_id)
        if post is None or post.is_deleted:
            raise HTTPException(
                status_code=404, detail="Post not found or was deleted."
            )
        post = Post(content=data.content, parent_id=data.parent_id, author_id=author_id)
        return await self.repo.save(post)
        

    async def update(self, post_id: int, data: PostUpdateRequest):
        post = await self.repo.get_post_by_id(post_id)
        if post is None or post.is_deleted:
            raise HTTPException(
                status_code=404, detail="Post not found or was deleted."
            )
        patch = data.model_dump(exclude_unset=True)
        for field, value in patch.items():
            setattr(post, field, value)

        return await self.repo.save(post)

    async def like(self, post_id: int):
        post = await self.repo.update_like(post_id)

        if post is None:
            raise HTTPException(
                status_code=404, detail="Post not found or was deleted."
            )
        return post

    async def delete(self, post_id: int):
        post = await self.repo.get_post_by_id(post_id)
        if post is None or post.is_deleted:
            raise HTTPException(
                status_code=404, detail="Post not found or was deleted."
            )

        await self.repo.delete(post)


def get_post_service(repo: PostRepositoryDeps):
    return PostService(repo)


PostServiceDeps = Annotated[PostService, Depends(get_post_service)]
