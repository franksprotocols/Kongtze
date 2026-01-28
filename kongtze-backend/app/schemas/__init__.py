"""API schemas for Kongtze backend"""

from app.schemas.user import (
    UserBase,
    UserCreateParent,
    UserCreateStudent,
    UserLogin,
    UserResponse,
    Token,
    TokenData,
)
from app.schemas.subject import SubjectBase, SubjectCreate, SubjectResponse
from app.schemas.study_session import (
    StudySessionBase,
    StudySessionCreate,
    StudySessionUpdate,
    StudySessionResponse,
)
from app.schemas.test import (
    QuestionBase,
    QuestionCreate,
    QuestionResponse,
    QuestionWithAnswer,
    TestBase,
    TestCreate,
    TestResponse,
    TestWithQuestions,
    TestSubmission,
    TestResultResponse,
    TestResultWithReview,
)
from app.schemas.homework import (
    HomeworkBase,
    HomeworkCreate,
    HomeworkUpdate,
    HomeworkResponse,
)
from app.schemas.class_note import (
    ClassNoteBase,
    ClassNoteCreate,
    ClassNoteUpdate,
    ClassNoteResponse,
    ClassNoteWithTopics,
    TopicBase,
    TopicResponse,
)
from app.schemas.reward import (
    RewardBase,
    RewardCreate,
    RewardResponse,
    GiftBase,
    GiftCreate,
    GiftResponse,
    LuckyDrawResult,
)

__all__ = [
    # User
    "UserBase",
    "UserCreateParent",
    "UserCreateStudent",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenData",
    # Subject
    "SubjectBase",
    "SubjectCreate",
    "SubjectResponse",
    # Study Session
    "StudySessionBase",
    "StudySessionCreate",
    "StudySessionUpdate",
    "StudySessionResponse",
    # Test
    "QuestionBase",
    "QuestionCreate",
    "QuestionResponse",
    "QuestionWithAnswer",
    "TestBase",
    "TestCreate",
    "TestResponse",
    "TestWithQuestions",
    "TestSubmission",
    "TestResultResponse",
    "TestResultWithReview",
    # Homework
    "HomeworkBase",
    "HomeworkCreate",
    "HomeworkUpdate",
    "HomeworkResponse",
    # Class Note
    "ClassNoteBase",
    "ClassNoteCreate",
    "ClassNoteUpdate",
    "ClassNoteResponse",
    "ClassNoteWithTopics",
    "TopicBase",
    "TopicResponse",
    # Reward
    "RewardBase",
    "RewardCreate",
    "RewardResponse",
    "GiftBase",
    "GiftCreate",
    "GiftResponse",
    "LuckyDrawResult",
]
