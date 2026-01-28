"""Test Context Builder Service for AI Test Generation"""

from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc

from app.models.test_result import TestResult
from app.models.student_profile import StudentProfile
from app.models.student_performance_analytics import StudentPerformanceAnalytics
from app.models.class_note import ClassNote
from app.models.homework import Homework
from app.models.test import Test
from app.models.question import Question


class TestContextBuilder:
    """Build comprehensive context for AI test generation"""

    async def build_context(
        self,
        user_id: int,
        subject_id: int,
        db: AsyncSession
    ) -> str:
        """
        Build comprehensive context for AI test generation

        Args:
            user_id: User ID
            subject_id: Subject ID
            db: Database session

        Returns:
            Formatted context string for AI
        """
        # 1. Get recent test history (last 10 tests)
        recent_tests = await self._get_recent_tests(user_id, subject_id, db)

        # 2. Get performance analytics
        analytics = await self._get_performance_analytics(user_id, subject_id, db)

        # 3. Get student profile
        profile = await self._get_student_profile(user_id, db)

        # 4. Get recent notes (last 2 weeks)
        notes = await self._get_recent_notes(user_id, subject_id, db)

        # 5. Get recent homework (last 2 weeks)
        homework = await self._get_recent_homework(user_id, subject_id, db)

        # 6. Build context string
        context = self._format_context(
            recent_tests, analytics, profile, notes, homework
        )

        return context

    async def _get_recent_tests(
        self,
        user_id: int,
        subject_id: int,
        db: AsyncSession,
        limit: int = 10
    ) -> List[dict]:
        """Get recent test results with scores and times"""
        result = await db.execute(
            select(TestResult, Test)
            .join(Test, TestResult.test_id == Test.test_id)
            .where(
                and_(
                    TestResult.user_id == user_id,
                    Test.subject_id == subject_id
                )
            )
            .order_by(desc(TestResult.submitted_at))
            .limit(limit)
        )

        test_data = []
        for test_result, test in result.all():
            test_data.append({
                "test_id": test.test_id,
                "title": test.title,
                "difficulty_level": test.difficulty_level,
                "score": test_result.score,
                "total_points": test_result.total_points,
                "time_taken": test_result.time_taken_seconds,
                "submitted_at": test_result.submitted_at
            })

        return test_data

    async def _get_performance_analytics(
        self,
        user_id: int,
        subject_id: int,
        db: AsyncSession
    ) -> Optional[StudentPerformanceAnalytics]:
        """Get student performance analytics"""
        result = await db.execute(
            select(StudentPerformanceAnalytics)
            .where(
                and_(
                    StudentPerformanceAnalytics.user_id == user_id,
                    StudentPerformanceAnalytics.subject_id == subject_id
                )
            )
        )
        return result.scalar_one_or_none()

    async def _get_student_profile(
        self,
        user_id: int,
        db: AsyncSession
    ) -> Optional[StudentProfile]:
        """Get student profile"""
        result = await db.execute(
            select(StudentProfile)
            .where(StudentProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def _get_recent_notes(
        self,
        user_id: int,
        subject_id: int,
        db: AsyncSession,
        weeks_back: int = 2
    ) -> List[ClassNote]:
        """Get notes from the last N weeks for a subject"""
        cutoff_date = datetime.now() - timedelta(weeks=weeks_back)

        result = await db.execute(
            select(ClassNote)
            .where(
                and_(
                    ClassNote.user_id == user_id,
                    ClassNote.subject_id == subject_id,
                    ClassNote.uploaded_at >= cutoff_date
                )
            )
            .order_by(desc(ClassNote.uploaded_at))
        )

        return result.scalars().all()

    async def _get_recent_homework(
        self,
        user_id: int,
        subject_id: int,
        db: AsyncSession,
        weeks_back: int = 2
    ) -> List[Homework]:
        """Get homework from the last N weeks for a subject"""
        cutoff_date = datetime.now() - timedelta(weeks=weeks_back)

        result = await db.execute(
            select(Homework)
            .where(
                and_(
                    Homework.user_id == user_id,
                    Homework.subject_id == subject_id,
                    Homework.uploaded_at >= cutoff_date
                )
            )
            .order_by(desc(Homework.uploaded_at))
        )

        return result.scalars().all()

    def _format_context(
        self,
        recent_tests: List[dict],
        analytics: Optional[StudentPerformanceAnalytics],
        profile: Optional[StudentProfile],
        notes: List[ClassNote],
        homework: List[Homework]
    ) -> str:
        """Format all context into a unified string for AI"""
        context_parts = []

        # Student Profile Section
        if profile:
            context_parts.append("=== STUDENT PROFILE ===")
            context_parts.append(f"Age: {profile.age} years old")
            context_parts.append(f"School: {profile.school_name}")
            context_parts.append(f"Grade: {profile.grade_level}")
            context_parts.append(f"\nSubject Proficiency:")
            context_parts.append(f"- Math: {profile.math_level}")
            context_parts.append(f"- English: {profile.english_level}")
            context_parts.append(f"- Chinese: {profile.chinese_level}")

            if profile.strengths:
                context_parts.append(f"\nStrengths: {', '.join(profile.strengths)}")
            if profile.weaknesses:
                context_parts.append(f"Weaknesses: {', '.join(profile.weaknesses)}")

            if profile.notes:
                context_parts.append(f"\nSpecial Notes: {profile.notes}")
            context_parts.append("")

        # Performance Analytics Section
        if analytics:
            context_parts.append("=== PERFORMANCE ANALYTICS ===")
            context_parts.append(f"Total Tests Taken: {analytics.total_tests_taken}")
            if analytics.average_score:
                context_parts.append(f"Average Score: {analytics.average_score}%")
            if analytics.current_difficulty_level:
                context_parts.append(f"Current Difficulty Level: {analytics.current_difficulty_level}/4")
            if analytics.recommended_difficulty_level:
                context_parts.append(f"Recommended Difficulty: {analytics.recommended_difficulty_level}/4")
            if analytics.difficulty_trend:
                context_parts.append(f"Trend: {analytics.difficulty_trend}")
            context_parts.append("")

        # Recent Test History Section
        if recent_tests:
            context_parts.append("=== RECENT TEST HISTORY (Last 10 Tests) ===")
            for i, test in enumerate(recent_tests, 1):
                percentage = (test["score"] / test["total_points"] * 100) if test["total_points"] > 0 else 0
                context_parts.append(
                    f"{i}. {test['title']} - "
                    f"Score: {test['score']}/{test['total_points']} ({percentage:.0f}%), "
                    f"Difficulty: {test['difficulty_level']}/4, "
                    f"Time: {test['time_taken']}s"
                )
            context_parts.append("")

        # Class Notes Section
        if notes:
            context_parts.append("=== RECENT CLASS NOTES (Last 2 Weeks) ===")
            for i, note in enumerate(notes, 1):
                title = note.title if note.title else f"Note {i}"
                context_parts.append(f"\nNote {i}: {title}")
                context_parts.append(f"Date: {note.uploaded_at.strftime('%Y-%m-%d')}")
                if note.ocr_text:
                    # Limit to first 500 characters
                    text_preview = note.ocr_text[:500]
                    if len(note.ocr_text) > 500:
                        text_preview += "..."
                    context_parts.append(f"Content: {text_preview}")
                context_parts.append("---")
            context_parts.append("")
        else:
            context_parts.append("=== RECENT CLASS NOTES ===")
            context_parts.append("No recent class notes available.")
            context_parts.append("")

        # Homework Section
        if homework:
            context_parts.append("=== RECENT HOMEWORK (Last 2 Weeks) ===")
            for i, hw in enumerate(homework, 1):
                context_parts.append(f"\nHomework {i}")
                context_parts.append(f"Date: {hw.uploaded_at.strftime('%Y-%m-%d')}")
                context_parts.append(f"Reviewed: {'Yes' if hw.is_reviewed else 'No'}")
                if hw.ocr_text:
                    # Limit to first 500 characters
                    text_preview = hw.ocr_text[:500]
                    if len(hw.ocr_text) > 500:
                        text_preview += "..."
                    context_parts.append(f"Content: {text_preview}")
                if hw.corrected_text:
                    text_preview = hw.corrected_text[:500]
                    if len(hw.corrected_text) > 500:
                        text_preview += "..."
                    context_parts.append(f"Corrected: {text_preview}")
                context_parts.append("---")
            context_parts.append("")
        else:
            context_parts.append("=== RECENT HOMEWORK ===")
            context_parts.append("No recent homework available.")
            context_parts.append("")

        # Instructions for AI
        context_parts.append("=== INSTRUCTIONS ===")
        context_parts.append("Please generate test questions that:")
        context_parts.append("1. Match the student's proficiency level and learning pace")
        context_parts.append("2. Are relevant to recent class notes and homework")
        context_parts.append("3. Address known weaknesses for improvement")
        context_parts.append("4. Build on demonstrated strengths")
        context_parts.append("5. Align with the student's current difficulty level and performance trend")

        return "\n".join(context_parts)

    async def get_relevant_content_ids(
        self,
        user_id: int,
        subject_id: int,
        db: AsyncSession,
        max_notes: int = 3,
        max_homework: int = 2,
        weeks_back: int = 2
    ) -> dict:
        """
        Automatically select relevant notes and homework IDs for test generation

        Args:
            user_id: User ID
            subject_id: Subject ID
            db: Database session
            max_notes: Maximum number of notes to select
            max_homework: Maximum number of homework to select
            weeks_back: How many weeks back to look

        Returns:
            Dictionary with note_ids and homework_ids lists
        """
        cutoff_date = datetime.now() - timedelta(weeks=weeks_back)

        # Get recent notes
        notes_result = await db.execute(
            select(ClassNote)
            .where(
                and_(
                    ClassNote.user_id == user_id,
                    ClassNote.subject_id == subject_id,
                    ClassNote.uploaded_at >= cutoff_date
                )
            )
            .order_by(desc(ClassNote.uploaded_at))
            .limit(max_notes)
        )
        notes = notes_result.scalars().all()

        # Get recent homework
        homework_result = await db.execute(
            select(Homework)
            .where(
                and_(
                    Homework.user_id == user_id,
                    Homework.subject_id == subject_id,
                    Homework.uploaded_at >= cutoff_date
                )
            )
            .order_by(desc(Homework.uploaded_at))
            .limit(max_homework)
        )
        homework = homework_result.scalars().all()

        return {
            "note_ids": [note.note_id for note in notes],
            "homework_ids": [hw.homework_id for hw in homework]
        }


# Create singleton instance
test_context_builder = TestContextBuilder()
