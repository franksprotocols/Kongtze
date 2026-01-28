"""Class note and topic schemas for API validation"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# Topic schemas
class TopicBase(BaseModel):
    """Base topic schema"""
    topic_name: str = Field(..., max_length=255)
    confidence: float = Field(..., ge=0.0, le=1.0)


class TopicResponse(TopicBase):
    """Schema for topic response"""
    topic_id: int
    note_id: int
    subject_id: int
    extracted_at: datetime

    class Config:
        from_attributes = True


# Class note schemas
class ClassNoteBase(BaseModel):
    """Base class note schema"""
    subject_id: int
    title: str = Field(..., max_length=255)


class ClassNoteCreate(ClassNoteBase):
    """Schema for creating class note (with photo upload)"""
    photo_path: str = Field(..., max_length=500)


class ClassNoteUpdate(BaseModel):
    """Schema for updating class note"""
    title: Optional[str] = Field(None, max_length=255)


class ClassNoteResponse(ClassNoteBase):
    """Schema for class note response"""
    note_id: int
    user_id: int
    photo_path: str
    ocr_text: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ClassNoteWithTopics(ClassNoteResponse):
    """Schema for class note with extracted topics"""
    topics: List[TopicResponse]
