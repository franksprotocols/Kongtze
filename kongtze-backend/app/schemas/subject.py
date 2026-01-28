"""Subject schemas for API validation"""

from typing import Optional
from pydantic import BaseModel, Field


class SubjectBase(BaseModel):
    """Base subject schema"""
    name: str = Field(..., max_length=100)
    display_name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class SubjectCreate(SubjectBase):
    """Schema for creating a subject"""
    pass


class SubjectResponse(SubjectBase):
    """Schema for subject response"""
    subject_id: int

    class Config:
        from_attributes = True
