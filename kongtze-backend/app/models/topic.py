from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Topic(Base):
    """Curriculum topics extracted from class notes (AI-generated)"""
    __tablename__ = "topics"

    topic_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("class_notes.note_id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"), nullable=False)

    # Topic information
    topic_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # IB curriculum context
    curriculum_context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    extracted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<Topic(topic_id={self.topic_id}, name='{self.topic_name}', subject_id={self.subject_id})>"
