"""Subject routes for Kongtze API"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.subject import Subject
from app.models.user import User
from app.schemas.subject import SubjectResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("", response_model=List[SubjectResponse])
async def get_subjects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[SubjectResponse]:
    """
    Get all available subjects.

    Returns a list of all subjects (Math, English, Chinese, Science).
    """
    result = await db.execute(select(Subject))
    subjects = result.scalars().all()

    return [SubjectResponse.model_validate(subject) for subject in subjects]


@router.get("/{subject_id}", response_model=SubjectResponse)
async def get_subject(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SubjectResponse:
    """
    Get a specific subject by ID.

    - **subject_id**: The subject ID
    """
    result = await db.execute(
        select(Subject).where(Subject.subject_id == subject_id)
    )
    subject = result.scalar_one_or_none()

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    return SubjectResponse.model_validate(subject)
