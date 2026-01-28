"""Homework schemas for API validation"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class HomeworkBase(BaseModel):
    """Base homework schema"""
    subject_id: int
    title: str = Field(..., max_length=255)


class HomeworkCreate(HomeworkBase):
    """Schema for creating homework (with photo upload)"""
    photo_path: str = Field(..., max_length=500)


class HomeworkUpdate(BaseModel):
    """Schema for updating homework"""
    title: Optional[str] = Field(None, max_length=255)
    parent_reviewed: Optional[bool] = None


class HomeworkResponse(HomeworkBase):
    """Schema for homework response"""
    homework_id: int
    user_id: int
    photo_path: str
    ocr_text: Optional[str] = None
    parent_reviewed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
