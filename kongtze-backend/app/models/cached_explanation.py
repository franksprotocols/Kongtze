from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class CachedExplanation(Base):
    """Cached AI explanations to reduce Gemini API costs"""
    __tablename__ = "cached_explanations"

    # SHA256 hash of question text as primary key
    question_hash: Mapped[str] = mapped_column(String(64), primary_key=True)

    # AI-generated explanation
    ai_explanation: Mapped[str] = mapped_column(Text, nullable=False)

    # Cache statistics
    hit_count: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_accessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<CachedExplanation(hash='{self.question_hash[:16]}...', hits={self.hit_count})>"
