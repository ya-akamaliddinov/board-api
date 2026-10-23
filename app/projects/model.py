from datetime import datetime

from sqlalchemy import String, false, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # String(280) скомпилируется в VARCHAR(280) — это корректно для PostgreSQL
    content: Mapped[str] = mapped_column(String(280))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(
        onupdate=func.now(), default=None
    )
    likes_count: Mapped[int] = mapped_column(default=0, server_default="0")
    is_deleted: Mapped[bool] = mapped_column(default=False, server_default=false())

    def __init__(
        self,
        content: str,
        likes_count: int | None = None,
        is_deleted: bool = False,
    ):
        self.content = content
        self.likes_count = likes_count
        self.is_deleted = is_deleted
