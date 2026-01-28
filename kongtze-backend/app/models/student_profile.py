from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON
from app.core.database import Base


class StudentProfile(Base):
    """Student profile for personalized test generation"""
    __tablename__ = "student_profiles"

    profile_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), unique=True, nullable=False)

    # Basic info
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    grade_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    school_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Subject proficiency levels
    math_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # 'beginner', 'intermediate', 'advanced', 'expert'
    english_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    chinese_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Specific strengths/weaknesses (JSON arrays)
    strengths: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # ["mental_math", "geometry", ...]
    weaknesses: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # ["chinese_writing", ...]

    # Learning style
    learning_pace: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # 'fast', 'moderate', 'slow'
    preferred_question_types: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # ["multiple_choice", ...]

    # Special considerations
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<StudentProfile(profile_id={self.profile_id}, user_id={self.user_id}, school={self.school_name})>"
