from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Boolean, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class AIPromptTemplate(Base):
    """AI prompt templates for test generation and other AI operations"""
    __tablename__ = "ai_prompt_templates"

    template_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    template_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    template_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # Types: 'test_generation', 'question_generation', 'schedule_generation', etc.

    prompt_template: Mapped[str] = mapped_column(Text, nullable=False)
    # Template with placeholders like {subject}, {difficulty_level}, {context}, etc.

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # System templates cannot be deleted, only modified

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<AIPromptTemplate(template_id={self.template_id}, name={self.template_name}, type={self.template_type})>"
