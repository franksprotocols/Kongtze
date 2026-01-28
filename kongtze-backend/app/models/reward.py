from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Reward(Base):
    """Reward points tracking for gamification"""
    __tablename__ = "rewards"

    reward_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)

    # Points transaction
    points: Mapped[int] = mapped_column(Integer, nullable=False)  # Can be negative for spending
    balance: Mapped[int] = mapped_column(Integer, nullable=False)  # Running balance

    # Source of points
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "test_completion", "lucky_draw", etc.
    source_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # test_id, etc.

    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<Reward(reward_id={self.reward_id}, user_id={self.user_id}, points={self.points}, balance={self.balance})>"
