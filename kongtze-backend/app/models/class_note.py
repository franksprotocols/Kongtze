from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class ClassNote(Base):
    """Class notes upload and OCR results"""
    __tablename__ = "class_notes"

    note_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"), nullable=False)

    # File storage path
    photo_path: Mapped[str] = mapped_column(String(500), nullable=False)

    # OCR results
    ocr_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Note metadata
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<ClassNote(note_id={self.note_id}, subject_id={self.subject_id}, title='{self.title}')>"
