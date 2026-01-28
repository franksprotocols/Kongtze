"""Adaptive Difficulty Service for Test Generation"""

from datetime import datetime, timedelta, date
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, func
from decimal import Decimal

from app.models.test_result import TestResult
from app.models.test import Test
from app.models.student_performance_analytics import StudentPerformanceAnalytics


class AdaptiveDifficultyService:
    """Service for calculating adaptive difficulty based on student performance"""

    # Thresholds for difficulty adjustment
    HIGH_SCORE_THRESHOLD = 85.0  # If avg score >= 85%, consider increasing
    LOW_SCORE_THRESHOLD = 70.0   # If avg score < 70%, consider decreasing
    MIN_TESTS_FOR_ADJUSTMENT = 3  # Minimum tests before adjusting difficulty

    # Time efficiency thresholds (seconds per question)
    FAST_TIME_MULTIPLIER = 0.8   # If time < 80% of expected, student is fast
    SLOW_TIME_MULTIPLIER = 1.2   # If time > 120% of expected, student is slow

    async def calculate_recommended_difficulty(
        self,
        user_id: int,
        subject_id: int,
        db: AsyncSession,
        lookback_tests: int = 5
    ) -> int:
        """
        Calculate recommended difficulty level based on recent performance

        Args:
            user_id: User ID
            subject_id: Subject ID
            db: Database session
            lookback_tests: Number of recent tests to analyze

        Returns:
            Recommended difficulty level (1-4)
        """
        # Get recent test results
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
            .limit(lookback_tests)
        )

        recent_tests = result.all()

        if len(recent_tests) < self.MIN_TESTS_FOR_ADJUSTMENT:
            # Not enough data, return default difficulty
            return 2

        # Calculate metrics
        total_score = 0
        total_points = 0
        total_time = 0
        total_questions = 0
        current_difficulty = 2

        for test_result, test in recent_tests:
            total_score += test_result.score
            total_points += test_result.total_points
            total_time += test_result.time_taken_seconds
            # Estimate questions from test (you may need to adjust this)
            total_questions += 10  # Default assumption
            current_difficulty = test.difficulty_level

        # Calculate average score percentage
        avg_score_pct = (total_score / total_points * 100) if total_points > 0 else 0

        # Calculate average time per question
        avg_time_per_question = total_time / total_questions if total_questions > 0 else 0

        # Expected time per question based on difficulty (rough estimates)
        expected_time_map = {1: 30, 2: 45, 3: 60, 4: 90}
        expected_time = expected_time_map.get(current_difficulty, 45)

        # Determine if student is fast or slow
        is_fast = avg_time_per_question < (expected_time * self.FAST_TIME_MULTIPLIER)
        is_slow = avg_time_per_question > (expected_time * self.SLOW_TIME_MULTIPLIER)

        # Calculate recommended difficulty
        recommended = current_difficulty

        if avg_score_pct >= self.HIGH_SCORE_THRESHOLD and is_fast:
            # Student is doing well and fast - increase difficulty
            recommended = min(current_difficulty + 1, 4)
        elif avg_score_pct >= self.HIGH_SCORE_THRESHOLD and not is_slow:
            # Student is doing well but not particularly fast - slight increase
            if avg_score_pct >= 90:
                recommended = min(current_difficulty + 1, 4)
        elif avg_score_pct < self.LOW_SCORE_THRESHOLD or is_slow:
            # Student is struggling - decrease difficulty
            recommended = max(current_difficulty - 1, 1)
        # else: maintain current difficulty

        return recommended

    async def update_performance_analytics(
        self,
        user_id: int,
        subject_id: int,
        db: AsyncSession,
        analysis_period_days: int = 30
    ) -> StudentPerformanceAnalytics:
        """
        Update or create performance analytics for a student

        Args:
            user_id: User ID
            subject_id: Subject ID
            db: Database session
            analysis_period_days: Number of days to analyze

        Returns:
            Updated StudentPerformanceAnalytics object
        """
        # Calculate period
        period_end = date.today()
        period_start = period_end - timedelta(days=analysis_period_days)

        # Get all test results in the period
        result = await db.execute(
            select(TestResult, Test)
            .join(Test, TestResult.test_id == Test.test_id)
            .where(
                and_(
                    TestResult.user_id == user_id,
                    Test.subject_id == subject_id,
                    TestResult.submitted_at >= datetime.combine(period_start, datetime.min.time())
                )
            )
            .order_by(TestResult.submitted_at)
        )

        test_results = result.all()

        if not test_results:
            # No tests in period, return empty analytics
            return None

        # Calculate overall metrics
        total_tests = len(test_results)
        total_score = sum(tr.score for tr, _ in test_results)
        total_points = sum(tr.total_points for tr, _ in test_results)
        total_time = sum(tr.time_taken_seconds for tr, _ in test_results)
        total_questions = total_tests * 10  # Estimate

        avg_score = Decimal(total_score / total_points * 100) if total_points > 0 else Decimal(0)
        avg_time_per_question = int(total_time / total_questions) if total_questions > 0 else 0

        # Get current difficulty from most recent test
        current_difficulty = test_results[-1][1].difficulty_level

        # Calculate recommended difficulty
        recommended_difficulty = await self.calculate_recommended_difficulty(
            user_id, subject_id, db
        )

        # Calculate difficulty breakdown
        difficulty_breakdown = await self._calculate_difficulty_breakdown(test_results)

        # Determine trend
        difficulty_trend = self._calculate_difficulty_trend(test_results)

        # Get or create analytics record
        analytics_result = await db.execute(
            select(StudentPerformanceAnalytics)
            .where(
                and_(
                    StudentPerformanceAnalytics.user_id == user_id,
                    StudentPerformanceAnalytics.subject_id == subject_id
                )
            )
        )
        analytics = analytics_result.scalar_one_or_none()

        if analytics:
            # Update existing
            analytics.total_tests_taken = total_tests
            analytics.average_score = avg_score
            analytics.average_time_per_question = avg_time_per_question
            analytics.current_difficulty_level = current_difficulty
            analytics.recommended_difficulty_level = recommended_difficulty
            analytics.difficulty_trend = difficulty_trend
            analytics.period_start = period_start
            analytics.period_end = period_end
            analytics.difficulty_breakdown = difficulty_breakdown
        else:
            # Create new
            analytics = StudentPerformanceAnalytics(
                user_id=user_id,
                subject_id=subject_id,
                total_tests_taken=total_tests,
                average_score=avg_score,
                average_time_per_question=avg_time_per_question,
                current_difficulty_level=current_difficulty,
                recommended_difficulty_level=recommended_difficulty,
                difficulty_trend=difficulty_trend,
                period_start=period_start,
                period_end=period_end,
                difficulty_breakdown=difficulty_breakdown
            )
            db.add(analytics)

        await db.commit()
        await db.refresh(analytics)

        return analytics

    async def _calculate_difficulty_breakdown(
        self,
        test_results: List[tuple]
    ) -> Dict:
        """
        Calculate performance breakdown by difficulty level

        Args:
            test_results: List of (TestResult, Test) tuples

        Returns:
            Dictionary with breakdown by difficulty
        """
        breakdown = {}

        for test_result, test in test_results:
            difficulty = str(test.difficulty_level)

            if difficulty not in breakdown:
                breakdown[difficulty] = {
                    "tests": 0,
                    "avg_score": 0,
                    "avg_time": 0,
                    "total_score": 0,
                    "total_points": 0,
                    "total_time": 0
                }

            breakdown[difficulty]["tests"] += 1
            breakdown[difficulty]["total_score"] += test_result.score
            breakdown[difficulty]["total_points"] += test_result.total_points
            breakdown[difficulty]["total_time"] += test_result.time_taken_seconds

        # Calculate averages
        for difficulty in breakdown:
            data = breakdown[difficulty]
            if data["total_points"] > 0:
                data["avg_score"] = round(data["total_score"] / data["total_points"] * 100, 2)
            if data["tests"] > 0:
                data["avg_time"] = round(data["total_time"] / data["tests"] / 10, 2)  # Per question estimate

            # Remove temporary totals
            del data["total_score"]
            del data["total_points"]
            del data["total_time"]

        return breakdown

    def _calculate_difficulty_trend(
        self,
        test_results: List[tuple]
    ) -> str:
        """
        Calculate difficulty trend based on recent performance

        Args:
            test_results: List of (TestResult, Test) tuples (ordered by time)

        Returns:
            Trend string: 'improving', 'stable', or 'declining'
        """
        if len(test_results) < 3:
            return "stable"

        # Split into first half and second half
        mid_point = len(test_results) // 2
        first_half = test_results[:mid_point]
        second_half = test_results[mid_point:]

        # Calculate average scores for each half
        first_half_score = sum(tr.score / tr.total_points for tr, _ in first_half if tr.total_points > 0) / len(first_half)
        second_half_score = sum(tr.score / tr.total_points for tr, _ in second_half if tr.total_points > 0) / len(second_half)

        # Compare
        diff = second_half_score - first_half_score

        if diff > 0.05:  # 5% improvement
            return "improving"
        elif diff < -0.05:  # 5% decline
            return "declining"
        else:
            return "stable"


    async def calculate_dynamic_question_count(
        self,
        user_id: int,
        subject_id: int,
        session_length_minutes: int,
        difficulty_level: int,
        db: AsyncSession
    ) -> int:
        """
        Calculate optimal number of questions for a test session

        Args:
            user_id: User ID
            subject_id: Subject ID
            session_length_minutes: Total session length in minutes
            difficulty_level: Test difficulty level (1-4)
            db: Database session

        Returns:
            Optimal number of questions
        """
        # Get student's average time per question from analytics
        analytics_result = await db.execute(
            select(StudentPerformanceAnalytics)
            .where(
                and_(
                    StudentPerformanceAnalytics.user_id == user_id,
                    StudentPerformanceAnalytics.subject_id == subject_id
                )
            )
        )
        analytics = analytics_result.scalar_one_or_none()

        # Base time estimates per question by difficulty (in seconds)
        base_time_map = {1: 30, 2: 45, 3: 60, 4: 90}
        base_time_per_question = base_time_map.get(difficulty_level, 45)

        # Adjust based on student's historical performance
        if analytics and analytics.average_time_per_question:
            # Use student's actual average, but cap adjustments
            student_avg = analytics.average_time_per_question
            # Blend base time with student's average (70% student, 30% base)
            estimated_time_per_question = int(student_avg * 0.7 + base_time_per_question * 0.3)
        else:
            estimated_time_per_question = base_time_per_question

        # Convert session length to seconds
        total_available_seconds = session_length_minutes * 60

        # Reserve 10% buffer time for review and transitions
        buffer_multiplier = 0.9
        usable_seconds = int(total_available_seconds * buffer_multiplier)

        # Calculate question count
        question_count = usable_seconds // estimated_time_per_question

        # Apply constraints
        min_questions = 5
        max_questions = 30

        question_count = max(min_questions, min(question_count, max_questions))

        return question_count

    def calculate_individual_time_limits(
        self,
        question_count: int,
        session_length_minutes: int,
        difficulty_level: int,
        question_types: Optional[List[str]] = None
    ) -> List[int]:
        """
        Calculate individual time limits for each question

        Args:
            question_count: Number of questions in the test
            session_length_minutes: Total session length in minutes
            difficulty_level: Test difficulty level (1-4)
            question_types: Optional list of question types for each question

        Returns:
            List of time limits in seconds for each question
        """
        # Base time per question by difficulty
        base_time_map = {1: 30, 2: 45, 3: 60, 4: 90}
        base_time = base_time_map.get(difficulty_level, 45)

        # Question type multipliers
        type_multipliers = {
            "multiple_choice": 1.0,
            "true_false": 0.7,
            "short_answer": 1.3,
            "essay": 2.0,
            "problem_solving": 1.5,
            "fill_blank": 0.9
        }

        # Calculate total available time (with 10% buffer)
        total_seconds = session_length_minutes * 60 * 0.9

        # If no question types provided, use uniform distribution
        if not question_types or len(question_types) != question_count:
            # Uniform time per question
            time_per_question = int(total_seconds / question_count)
            return [time_per_question] * question_count

        # Calculate weighted time allocation
        time_limits = []
        total_weight = sum(type_multipliers.get(qt, 1.0) for qt in question_types)

        for question_type in question_types:
            multiplier = type_multipliers.get(question_type, 1.0)
            # Allocate time proportionally based on type
            time_limit = int((base_time * multiplier / total_weight) * total_seconds / base_time)
            time_limits.append(max(15, time_limit))  # Minimum 15 seconds per question

        # Adjust to fit exactly within session length
        current_total = sum(time_limits)
        if current_total != total_seconds:
            # Distribute difference proportionally
            adjustment_factor = total_seconds / current_total
            time_limits = [int(t * adjustment_factor) for t in time_limits]

        return time_limits


# Create singleton instance
adaptive_difficulty_service = AdaptiveDifficultyService()
