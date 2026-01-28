from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class User(Base):
    """User model for both parent and student"""
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)  # Parent only
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Parent only
    pin: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)  # Student only (4-digit)
    is_parent: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id}, name='{self.name}', is_parent={self.is_parent})>"
