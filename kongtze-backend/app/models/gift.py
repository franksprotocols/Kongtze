from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Gift(Base):
    """Gift catalog for lucky draw (parent-configurable)"""
    __tablename__ = "gifts"

    gift_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Lucky draw tier: "gold", "silver", "bronze"
    tier: Mapped[str] = mapped_column(String(20), nullable=False)

    # Cost in points (for redemption system)
    points_cost: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Image path
    image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<Gift(gift_id={self.gift_id}, name='{self.name}', tier='{self.tier}')>"
