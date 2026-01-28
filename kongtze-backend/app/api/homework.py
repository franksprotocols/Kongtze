"""Homework routes for Kongtze API"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.models.homework import Homework
from app.models.subject import Subject
from app.models.user import User
from app.schemas.homework import HomeworkResponse, HomeworkUpdate
from app.api.deps import get_current_user, get_current_parent
from app.services.ocr_service import ocr_service
from app.services.file_storage import file_storage

router = APIRouter(prefix="/homework", tags=["Homework"])


@router.post("", response_model=HomeworkResponse, status_code=status.HTTP_201_CREATED)
async def upload_homework(
    subject_id: int = Form(...),
    title: str = Form(...),
    photo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HomeworkResponse:
    """
    Upload homework photo with OCR text extraction.

    - **subject_id**: Subject ID
    - **title**: Homework title
    - **photo**: Image file (JPG, PNG, etc.)
    """
    # Verify subject exists
    result = await db.execute(
        select(Subject).where(Subject.subject_id == subject_id)
    )
    subject = result.scalar_one_or_none()

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    # Validate image file
    file_content = await photo.read()
    await photo.seek(0)  # Reset file pointer

    is_valid = await ocr_service.validate_image(file_content)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file. Please upload a valid image (JPG, PNG, etc.)",
        )

    # Save file
    relative_path, absolute_path = await file_storage.save_upload(
        file=photo,
        category="homework",
        user_id=current_user.user_id,
    )

    # Extract text using OCR
    ocr_text = await ocr_service.extract_text_from_image(absolute_path)

    # Create homework record
    new_homework = Homework(
        user_id=current_user.user_id,
        subject_id=subject_id,
        title=title,
        photo_path=relative_path,
        ocr_text=ocr_text,
        parent_reviewed=False,
    )

    db.add(new_homework)
    await db.flush()
    await db.refresh(new_homework)

    return HomeworkResponse.model_validate(new_homework)


@router.get("", response_model=List[HomeworkResponse])
async def get_homework_list(
    subject_id: int = None,
    reviewed: bool = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[HomeworkResponse]:
    """
    Get all homework for the current user, with optional filters.

    - **subject_id**: Optional subject filter
    - **reviewed**: Optional filter for parent review status
    """
    query = select(Homework).where(Homework.user_id == current_user.user_id)

    if subject_id:
        query = query.where(Homework.subject_id == subject_id)

    if reviewed is not None:
        query = query.where(Homework.parent_reviewed == reviewed)

    query = query.order_by(Homework.created_at.desc())

    result = await db.execute(query)
    homework_list = result.scalars().all()

    return [HomeworkResponse.model_validate(hw) for hw in homework_list]


@router.get("/{homework_id}", response_model=HomeworkResponse)
async def get_homework(
    homework_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HomeworkResponse:
    """
    Get a specific homework by ID.

    - **homework_id**: The homework ID
    """
    result = await db.execute(
        select(Homework).where(
            and_(
                Homework.homework_id == homework_id,
                Homework.user_id == current_user.user_id,
            )
        )
    )
    homework = result.scalar_one_or_none()

    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Homework not found",
        )

    return HomeworkResponse.model_validate(homework)


@router.put("/{homework_id}", response_model=HomeworkResponse)
async def update_homework(
    homework_id: int,
    update_data: HomeworkUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HomeworkResponse:
    """
    Update homework (parent can mark as reviewed).

    - **homework_id**: The homework ID
    - **title**: Optional new title
    - **parent_reviewed**: Optional review status (parent only)
    """
    # Get homework
    result = await db.execute(
        select(Homework).where(
            and_(
                Homework.homework_id == homework_id,
                Homework.user_id == current_user.user_id,
            )
        )
    )
    homework = result.scalar_one_or_none()

    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Homework not found",
        )

    # Update fields if provided
    update_dict = update_data.model_dump(exclude_unset=True)

    # Only parents can mark as reviewed
    if "parent_reviewed" in update_dict and not current_user.is_parent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can mark homework as reviewed",
        )

    for field, value in update_dict.items():
        setattr(homework, field, value)

    await db.flush()
    await db.refresh(homework)

    return HomeworkResponse.model_validate(homework)


@router.delete("/{homework_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_homework(
    homework_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete homework.

    - **homework_id**: The homework ID
    """
    # Get homework
    result = await db.execute(
        select(Homework).where(
            and_(
                Homework.homework_id == homework_id,
                Homework.user_id == current_user.user_id,
            )
        )
    )
    homework = result.scalar_one_or_none()

    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Homework not found",
        )

    # Delete file from storage
    file_storage.delete_file(homework.photo_path)

    # Delete database record
    await db.delete(homework)
