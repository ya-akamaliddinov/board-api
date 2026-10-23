from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, update

from app.core.db import DBSessionDeps
from app.projects.model import Post


class PostRepository:
    def __init__(self, session: DBSessionDeps):
        self.session = session

    async def get_post_by_id(self, post_id: int):
        res = await self.session.get(Post, post_id)
        return res

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

    async def update_like(self, post_id: int, post: Post):
        update_query = (
            update(Post)
            .where(Post.id == post_id, Post.is_deleted == False)
            .values(likes_count=Post.likes_count + 1)
            .returning(Post)
        )
        await self.session.execute(update_query)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def delete(self, post: Post):
        post.is_deleted = True
        await self.session.commit()
        await self.session.refresh(post)


def get_post_repository(session: DBSessionDeps):
    return PostRepository(session)


PostRepositoryDeps = Annotated[PostRepository, Depends(get_post_repository)]
