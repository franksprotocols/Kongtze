from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Homework(Base):
    """Homework upload and OCR results"""
    __tablename__ = "homework"

    homework_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"), nullable=False)

    # File storage path
    photo_path: Mapped[str] = mapped_column(String(500), nullable=False)

    # OCR results
    ocr_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Parent review and correction
    corrected_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_reviewed: Mapped[bool] = mapped_column(Boolean, default=False)

    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<Homework(homework_id={self.homework_id}, subject_id={self.subject_id}, reviewed={self.is_reviewed})>"
