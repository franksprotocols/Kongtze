"""Study session schemas for API validation"""

from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, Field


class StudySessionBase(BaseModel):
    """Base study session schema"""
    subject_id: int
    day_of_week: int = Field(..., ge=0, le=6, description="0=Monday, 6=Sunday")
    start_time: time
    duration_minutes: int = Field(default=30, ge=15, le=120)
    difficulty_level: Optional[int] = Field(default=2, ge=1, le=4, description="1=beginner, 2=intermediate, 3=advanced, 4=expert")
    title: Optional[str] = Field(None, max_length=255)


class StudySessionCreate(StudySessionBase):
    """Schema for creating a study session"""
    pass


class StudySessionUpdate(BaseModel):
    """Schema for updating a study session"""
    subject_id: Optional[int] = None
    day_of_week: Optional[int] = Field(None, ge=0, le=6)
    start_time: Optional[time] = None
    duration_minutes: Optional[int] = Field(None, ge=15, le=120)
    difficulty_level: Optional[int] = Field(None, ge=1, le=4)
    title: Optional[str] = Field(None, max_length=255)


class StudySessionResponse(StudySessionBase):
    """Schema for study session response"""
    session_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
