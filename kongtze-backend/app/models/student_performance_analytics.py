from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, Numeric, Date, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON
from app.core.database import Base


class StudentPerformanceAnalytics(Base):
    """Student performance analytics for adaptive test generation"""
    __tablename__ = "student_performance_analytics"

    analytics_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"), nullable=False)

    # Performance metrics
    total_tests_taken: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_score: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)  # 0-100
    average_time_per_question: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # seconds

    # Difficulty progression
    current_difficulty_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-4
    recommended_difficulty_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-4
    difficulty_trend: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # 'improving', 'stable', 'declining'

    # Time period
    period_start: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    period_end: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Detailed breakdown by difficulty
    difficulty_breakdown: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    # Format: {
    #   "1": {"tests": 5, "avg_score": 95, "avg_time": 40},
    #   "2": {"tests": 3, "avg_score": 80, "avg_time": 55},
    #   ...
    # }

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<StudentPerformanceAnalytics(analytics_id={self.analytics_id}, user_id={self.user_id}, subject_id={self.subject_id})>"
