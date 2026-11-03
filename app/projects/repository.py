from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.core.db import DBSessionDeps
from app.projects.model import Post


class PostRepository:
    def __init__(self, session: DBSessionDeps):
        self.session = session

    async def get_latest_post_by_author(self, author_id: int) -> Post | None:
        query = (
            select(Post)
            .where(Post.author_id == author_id,)
            .order_by(Post.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_post_by_id(self, post_id: int):
        query = (
        select(Post)
        .where(Post.is_deleted == False)
        .options(selectinload(Post.replies.and_(Post.is_deleted==False))) # Сразу подгружаем ответы!
        .where(Post.id == post_id)
    )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def search(self, offset: int, limit: int):
        query = (
            select(Post)
            .order_by(Post.created_at.desc(), Post.id.desc())
            .offset(offset)
            .limit(limit)
            .where(Post.is_deleted == False)
        )
        result = await self.session.execute(query)
        posts = list(result.scalars().all())

        return posts

    async def save(self, post: Post):
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def update_like(self, post_id: int) -> Post | None:
        update_query = (
            update(Post)
            .where(Post.id == post_id, Post.is_deleted == False)
            .values(likes_count=Post.likes_count + 1)
            .returning(Post)
        )
        result = await self.session.execute(update_query)
        updated_post = result.scalar_one_or_none()

        await self.session.commit()
        return updated_post

    async def delete(self, post: Post):
        post.is_deleted = True
        await self.session.commit()
        await self.session.refresh(post)


def get_post_repository(session: DBSessionDeps):
    return PostRepository(session)


PostRepositoryDeps = Annotated[PostRepository, Depends(get_post_repository)]
