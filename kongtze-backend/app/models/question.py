from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Question(Base):
    """Question model for test questions"""
    __tablename__ = "questions"

    question_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.test_id"), nullable=False)

    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_order: Mapped[int] = mapped_column(Integer, nullable=False)  # Order in test

    # Answer options (for multiple choice)
    options: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # {"A": "...", "B": "...", ...}

    correct_answer: Mapped[str] = mapped_column(String(500), nullable=False)

    # Time limit for this specific question (seconds)
    time_limit_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    # Points awarded for correct answer
    points: Mapped[int] = mapped_column(Integer, default=10)

    def __repr__(self) -> str:
        return f"<Question(question_id={self.question_id}, test_id={self.test_id}, order={self.question_order})>"
