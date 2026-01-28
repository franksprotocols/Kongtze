from datetime import datetime, time
from typing import Optional
from sqlalchemy import String, Integer, Time, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class StudySession(Base):
    """Study session for weekly calendar scheduling"""
    __tablename__ = "study_sessions"

    session_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"), nullable=False)

    # Day of week: 0=Monday, 1=Tuesday, ..., 6=Sunday
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)

    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<StudySession(session_id={self.session_id}, day={self.day_of_week}, time={self.start_time})>"
