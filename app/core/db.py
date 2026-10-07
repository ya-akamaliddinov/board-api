from typing import AsyncGenerator, Annotated

from fastapi import Depends

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.settings import Settings


settings = Settings()  # type: ignore[call-arg]


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True
    )

async_session_local = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_local() as session:
        yield session


DBSessionDeps = Annotated[
    AsyncSession,
    Depends(get_session)
]
