from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Test(Base):
    """Test model for generated tests"""
    __tablename__ = "tests"

    test_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"), nullable=False)

    # Difficulty: 1=Beginner, 2=Intermediate, 3=Advanced, 4=Expert
    difficulty_level: Mapped[int] = mapped_column(Integer, nullable=False)

    # Time limit in minutes
    time_limit_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    # Total number of questions
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)

    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Test generation metadata
    source_note_ids: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # JSON array as string
    source_homework_ids: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # JSON array as string
    generation_mode: Mapped[str] = mapped_column(String(50), nullable=False, default="pure_ai")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<Test(test_id={self.test_id}, subject_id={self.subject_id}, difficulty={self.difficulty_level})>"
