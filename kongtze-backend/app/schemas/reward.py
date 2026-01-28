"""Reward and gift schemas for API validation"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# Reward schemas
class RewardBase(BaseModel):
    """Base reward schema"""
    points: int
    reason: str = Field(..., max_length=255)


class RewardCreate(RewardBase):
    """Schema for creating a reward transaction"""
    pass


class RewardResponse(RewardBase):
    """Schema for reward response"""
    reward_id: int
    user_id: int
    balance: int
    created_at: datetime

    class Config:
        from_attributes = True


# Gift schemas
class GiftBase(BaseModel):
    """Base gift schema"""
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    tier: str = Field(..., pattern=r"^(gold|silver|bronze)$")
    probability: float = Field(..., ge=0.0, le=1.0)


class GiftCreate(GiftBase):
    """Schema for creating a gift"""
    image_path: Optional[str] = Field(None, max_length=500)


class GiftResponse(GiftBase):
    """Schema for gift response"""
    gift_id: int
    image_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LuckyDrawResult(BaseModel):
    """Schema for lucky draw result"""
    gift: GiftResponse
    points_spent: int
    remaining_balance: int
