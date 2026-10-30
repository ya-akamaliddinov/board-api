from datetime import datetime
from typing import List

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(256), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    posts: Mapped[List["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __init__(self, email: str, password_hash: str):
        self.email = email
        self.password_hash = password_hash

