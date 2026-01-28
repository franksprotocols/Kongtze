"""Database models for Kongtze backend"""

from app.models.user import User
from app.models.subject import Subject
from app.models.study_session import StudySession
from app.models.test import Test
from app.models.question import Question
from app.models.test_result import TestResult
from app.models.homework import Homework
from app.models.class_note import ClassNote
from app.models.topic import Topic
from app.models.reward import Reward
from app.models.gift import Gift
from app.models.cached_explanation import CachedExplanation
from app.models.student_profile import StudentProfile
from app.models.student_performance_analytics import StudentPerformanceAnalytics
from app.models.ai_prompt_template import AIPromptTemplate

__all__ = [
    "User",
    "Subject",
    "StudySession",
    "Test",
    "Question",
    "TestResult",
    "Homework",
    "ClassNote",
    "Topic",
    "Reward",
    "Gift",
    "CachedExplanation",
    "StudentProfile",
    "StudentPerformanceAnalytics",
    "AIPromptTemplate",
]
