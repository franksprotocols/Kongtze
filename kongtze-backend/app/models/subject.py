from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Subject(Base):
    """Subject model for Math, English, Chinese, Science"""
    __tablename__ = "subjects"

    subject_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<Subject(subject_id={self.subject_id}, name='{self.name}')>"
