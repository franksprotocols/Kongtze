"""Test, Question, and TestResult schemas for API validation"""

from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


# Question schemas
class QuestionBase(BaseModel):
    """Base question schema"""
    question_text: str
    options: Dict[str, str] = Field(..., description="Options A, B, C, D")
    correct_answer: str = Field(..., pattern=r"^[A-D]$")
    time_limit_seconds: int = Field(default=60, ge=10, le=300)


class QuestionCreate(QuestionBase):
    """Schema for creating a question"""
    pass


class QuestionResponse(QuestionBase):
    """Schema for question response (without correct answer)"""
    question_id: int
    test_id: int

    class Config:
        from_attributes = True


class QuestionWithAnswer(QuestionResponse):
    """Schema for question response with correct answer (for review)"""
    correct_answer: str


# Test schemas
class TestBase(BaseModel):
    """Base test schema"""
    subject_id: int
    title: str = Field(..., max_length=255)
    difficulty_level: int = Field(..., ge=1, le=4, description="1=Beginner, 4=Expert")
    time_limit_minutes: int = Field(default=30, ge=5, le=120)
    total_questions: int = Field(default=10, ge=1, le=50)


class TestCreate(TestBase):
    """Schema for creating a test (AI generates questions)"""
    note_ids: Optional[List[int]] = Field(default=None, description="Optional note IDs for context-based generation")
    homework_ids: Optional[List[int]] = Field(default=None, description="Optional homework IDs for context-based generation")
    generation_mode: str = Field(default="pure_ai", pattern=r"^(pure_ai|notes_based|homework_based)$")


class TestResponse(TestBase):
    """Schema for test response"""
    test_id: int
    user_id: int
    created_at: datetime
    source_note_ids: Optional[List[int]] = None
    source_homework_ids: Optional[List[int]] = None
    generation_mode: str = "pure_ai"

    class Config:
        from_attributes = True


class TestWithQuestions(TestResponse):
    """Schema for test with its questions"""
    questions: List[QuestionResponse]


# Test result schemas
class TestSubmission(BaseModel):
    """Schema for submitting test answers"""
    test_id: int
    answers: Dict[str, str] = Field(..., description="Map of question_id to answer (A/B/C/D)")
    time_taken_seconds: int


class TestResultResponse(BaseModel):
    """Schema for test result response"""
    result_id: int
    test_id: int
    user_id: int
    score: int
    total_score: int
    time_taken_seconds: int
    answers: Dict[str, str]
    reward_points: int
    completed_at: datetime

    class Config:
        from_attributes = True


class TestResultWithReview(TestResultResponse):
    """Schema for test result with detailed review"""
    questions: List[QuestionWithAnswer]
    percentage: float = Field(..., description="Score percentage (0-100)")
