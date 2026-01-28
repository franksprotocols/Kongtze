from datetime import datetime
from sqlalchemy import Integer, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class TestResult(Base):
    """Test result model for submitted tests"""
    __tablename__ = "test_results"

    result_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.test_id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)

    # Answers submitted (question_id -> answer mapping)
    answers: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Score and timing
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total_points: Mapped[int] = mapped_column(Integer, nullable=False)
    time_taken_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    # Reward points earned
    reward_points: Mapped[int] = mapped_column(Integer, default=0)

    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<TestResult(result_id={self.result_id}, test_id={self.test_id}, score={self.score}/{self.total_points})>"
