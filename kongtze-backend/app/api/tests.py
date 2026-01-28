"""Test routes for Kongtze API"""

from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import json

from app.core.database import get_db
from app.models.test import Test
from app.models.question import Question
from app.models.test_result import TestResult
from app.models.subject import Subject
from app.models.user import User
from app.models.reward import Reward
from app.models.class_note import ClassNote
from app.models.homework import Homework
from app.schemas.test import (
    TestCreate,
    TestResponse,
    TestWithQuestions,
    QuestionResponse,
    QuestionWithAnswer,
    TestSubmission,
    TestResultResponse,
    TestResultWithReview,
)
from app.api.deps import get_current_user
from app.services.ai_service import ai_service

router = APIRouter(prefix="/tests", tags=["Tests"])


@router.post("", response_model=TestWithQuestions, status_code=status.HTTP_201_CREATED)
async def create_test(
    test_data: TestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TestWithQuestions:
    """
    Generate a new test with AI-powered questions.

    - **subject_id**: Subject ID
    - **title**: Test title
    - **difficulty_level**: 1=Beginner, 2=Intermediate, 3=Advanced, 4=Expert
    - **time_limit_minutes**: Total time limit (default: 30)
    - **total_questions**: Number of questions (default: 10)
    - **note_ids**: Optional list of note IDs for context-based generation
    - **homework_ids**: Optional list of homework IDs for context-based generation
    - **generation_mode**: Generation mode (pure_ai, notes_based, homework_based)
    """
    # Verify subject exists
    result = await db.execute(
        select(Subject).where(Subject.subject_id == test_data.subject_id)
    )
    subject = result.scalar_one_or_none()

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    # Fetch context from notes/homework if provided
    context_text = None
    context_parts = []

    if test_data.note_ids:
        # Fetch notes
        result = await db.execute(
            select(ClassNote).where(
                and_(
                    ClassNote.note_id.in_(test_data.note_ids),
                    ClassNote.user_id == current_user.user_id,
                )
            )
        )
        notes = result.scalars().all()

        # Verify all notes were found and belong to user
        if len(notes) != len(test_data.note_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more notes not found or do not belong to you",
            )

        # Concatenate OCR text from notes
        for i, note in enumerate(notes, 1):
            if note.ocr_text:
                context_parts.append(f"--- Note {i}: {note.title} ---\n{note.ocr_text}")

    if test_data.homework_ids:
        # Fetch homework
        result = await db.execute(
            select(Homework).where(
                and_(
                    Homework.homework_id.in_(test_data.homework_ids),
                    Homework.user_id == current_user.user_id,
                )
            )
        )
        homework_list = result.scalars().all()

        # Verify all homework were found and belong to user
        if len(homework_list) != len(test_data.homework_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more homework not found or do not belong to you",
            )

        # Concatenate OCR text from homework
        for i, hw in enumerate(homework_list, 1):
            if hw.ocr_text:
                context_parts.append(f"--- Homework {i}: {hw.title} ---\n{hw.ocr_text}")

    # Combine all context
    if context_parts:
        context_text = "\n\n".join(context_parts)

    # Create test record
    new_test = Test(
        user_id=current_user.user_id,
        subject_id=test_data.subject_id,
        title=test_data.title,
        difficulty_level=test_data.difficulty_level,
        time_limit_minutes=test_data.time_limit_minutes,
        total_questions=test_data.total_questions,
        source_note_ids=json.dumps(test_data.note_ids) if test_data.note_ids else None,
        source_homework_ids=json.dumps(test_data.homework_ids) if test_data.homework_ids else None,
        generation_mode=test_data.generation_mode,
    )

    db.add(new_test)
    await db.flush()
    await db.refresh(new_test)

    # Generate questions using AI
    ai_questions = await ai_service.generate_test_questions(
        subject=subject.display_name,
        difficulty_level=test_data.difficulty_level,
        num_questions=test_data.total_questions,
        context_text=context_text,
    )

    # Create question records
    questions = []
    for idx, q_data in enumerate(ai_questions):
        question = Question(
            test_id=new_test.test_id,
            question_text=q_data["question_text"],
            question_order=idx + 1,  # 1-based ordering
            options=q_data["options"],
            correct_answer=q_data["correct_answer"],
            time_limit_seconds=q_data.get("time_limit_seconds", 60),
        )
        db.add(question)
        questions.append(question)

    await db.flush()

    # Refresh questions to get IDs
    for question in questions:
        await db.refresh(question)

    # Return test with questions (without correct answers)
    test_response = TestResponse.model_validate(new_test)
    question_responses = [
        QuestionResponse.model_validate(q) for q in questions
    ]

    return TestWithQuestions(
        **test_response.model_dump(),
        questions=question_responses,
    )


@router.get("", response_model=List[TestResponse])
async def get_tests(
    subject_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[TestResponse]:
    """
    Get all tests for the current user, optionally filtered by subject.

    - **subject_id**: Optional subject filter
    """
    query = select(Test).where(Test.user_id == current_user.user_id)

    if subject_id:
        query = query.where(Test.subject_id == subject_id)

    query = query.order_by(Test.created_at.desc())

    result = await db.execute(query)
    tests = result.scalars().all()

    return [TestResponse.model_validate(test) for test in tests]


@router.get("/{test_id}", response_model=TestWithQuestions)
async def get_test(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TestWithQuestions:
    """
    Get a specific test with its questions (without showing correct answers).

    - **test_id**: The test ID
    """
    # Get test
    result = await db.execute(
        select(Test).where(
            and_(
                Test.test_id == test_id,
                Test.user_id == current_user.user_id,
            )
        )
    )
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found",
        )

    # Get questions
    result = await db.execute(
        select(Question).where(Question.test_id == test_id)
    )
    questions = result.scalars().all()

    test_response = TestResponse.model_validate(test)
    question_responses = [
        QuestionResponse.model_validate(q) for q in questions
    ]

    return TestWithQuestions(
        **test_response.model_dump(),
        questions=question_responses,
    )


@router.post("/submit", response_model=TestResultResponse)
async def submit_test(
    submission: TestSubmission,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TestResultResponse:
    """
    Submit test answers and get results with rewards.

    - **test_id**: The test ID
    - **answers**: Map of question_id to answer (A/B/C/D)
    - **time_taken_seconds**: Time taken to complete the test
    """
    # Get test
    result = await db.execute(
        select(Test).where(
            and_(
                Test.test_id == submission.test_id,
                Test.user_id == current_user.user_id,
            )
        )
    )
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found",
        )

    # Get questions
    result = await db.execute(
        select(Question).where(Question.test_id == submission.test_id)
    )
    questions = result.scalars().all()

    # Calculate score
    score = 0
    total_score = len(questions)

    for question in questions:
        user_answer = submission.answers.get(str(question.question_id))
        if user_answer == question.correct_answer:
            score += 1

    # Calculate reward points (1 point per correct answer, bonus for perfect score)
    reward_points = score
    if score == total_score:
        reward_points += 5  # Bonus for perfect score

    # Create test result
    test_result = TestResult(
        test_id=submission.test_id,
        user_id=current_user.user_id,
        score=score,
        total_score=total_score,
        time_taken_seconds=submission.time_taken_seconds,
        answers=submission.answers,
        reward_points=reward_points,
    )

    db.add(test_result)
    await db.flush()
    await db.refresh(test_result)

    # Get current user's reward balance
    balance_result = await db.execute(
        select(Reward)
        .where(Reward.user_id == current_user.user_id)
        .order_by(Reward.created_at.desc())
        .limit(1)
    )
    last_reward = balance_result.scalar_one_or_none()
    current_balance = last_reward.balance if last_reward else 0

    # Add reward transaction
    reward = Reward(
        user_id=current_user.user_id,
        points=reward_points,
        reason=f"Completed test: {test.title} ({score}/{total_score})",
        balance=current_balance + reward_points,
    )

    db.add(reward)
    await db.flush()

    return TestResultResponse.model_validate(test_result)


@router.get("/results/{result_id}", response_model=TestResultWithReview)
async def get_test_result(
    result_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TestResultWithReview:
    """
    Get detailed test result with review (shows correct answers and explanations).

    - **result_id**: The test result ID
    """
    # Get test result
    result = await db.execute(
        select(TestResult).where(
            and_(
                TestResult.result_id == result_id,
                TestResult.user_id == current_user.user_id,
            )
        )
    )
    test_result = result.scalar_one_or_none()

    if not test_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test result not found",
        )

    # Get questions
    result = await db.execute(
        select(Question).where(Question.test_id == test_result.test_id)
    )
    questions = result.scalars().all()

    # Build response with correct answers
    question_responses = [
        QuestionWithAnswer.model_validate(q) for q in questions
    ]

    result_response = TestResultResponse.model_validate(test_result)
    percentage = (test_result.score / test_result.total_score * 100) if test_result.total_score > 0 else 0

    return TestResultWithReview(
        **result_response.model_dump(),
        questions=question_responses,
        percentage=percentage,
    )


@router.get("/results", response_model=List[TestResultResponse])
async def get_test_results(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[TestResultResponse]:
    """
    Get all test results for the current user.
    """
    result = await db.execute(
        select(TestResult)
        .where(TestResult.user_id == current_user.user_id)
        .order_by(TestResult.completed_at.desc())
    )
    test_results = result.scalars().all()

    return [TestResultResponse.model_validate(tr) for tr in test_results]
