"""Class notes routes for Kongtze API"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.models.class_note import ClassNote
from app.models.topic import Topic
from app.models.subject import Subject
from app.models.user import User
from app.schemas.class_note import ClassNoteResponse, ClassNoteWithTopics, ClassNoteUpdate
from app.api.deps import get_current_user
from app.services.ocr_service import ocr_service
from app.services.ai_service import ai_service
from app.services.file_storage import file_storage

router = APIRouter(prefix="/class-notes", tags=["Class Notes"])


@router.post("", response_model=ClassNoteWithTopics, status_code=status.HTTP_201_CREATED)
async def upload_class_note(
    subject_id: int = Form(...),
    title: str = Form(...),
    photo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClassNoteWithTopics:
    """
    Upload class note photo with OCR and AI topic extraction.

    - **subject_id**: Subject ID
    - **title**: Class note title
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
        category="class_notes",
        user_id=current_user.user_id,
    )

    # Extract text using OCR
    ocr_text = await ocr_service.extract_text_from_image(absolute_path)

    # Create class note record
    new_note = ClassNote(
        user_id=current_user.user_id,
        subject_id=subject_id,
        title=title,
        photo_path=relative_path,
        ocr_text=ocr_text,
    )

    db.add(new_note)
    await db.flush()
    await db.refresh(new_note)

    # Extract topics using AI (if OCR text is available)
    topics = []
    if ocr_text and len(ocr_text) > 20:  # Only extract if sufficient text
        ai_topics = await ai_service.extract_topics_from_notes(
            ocr_text=ocr_text,
            subject=subject.display_name,
        )

        # Create topic records
        for topic_data in ai_topics:
            topic = Topic(
                note_id=new_note.note_id,
                subject_id=subject_id,
                topic_name=topic_data["topic"],
                confidence=topic_data["confidence"],
            )
            db.add(topic)
            topics.append(topic)

        await db.flush()

        # Refresh topics to get IDs
        for topic in topics:
            await db.refresh(topic)

    # Build response
    note_response = ClassNoteResponse.model_validate(new_note)
    topic_responses = [TopicResponse.model_validate(t) for t in topics]

    from app.schemas.class_note import TopicResponse

    return ClassNoteWithTopics(
        **note_response.model_dump(),
        topics=topic_responses,
    )


@router.get("", response_model=List[ClassNoteResponse])
async def get_class_notes(
    subject_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ClassNoteResponse]:
    """
    Get all class notes for the current user, with optional subject filter.

    - **subject_id**: Optional subject filter
    """
    query = select(ClassNote).where(ClassNote.user_id == current_user.user_id)

    if subject_id:
        query = query.where(ClassNote.subject_id == subject_id)

    query = query.order_by(ClassNote.created_at.desc())

    result = await db.execute(query)
    notes = result.scalars().all()

    return [ClassNoteResponse.model_validate(note) for note in notes]


@router.get("/{note_id}", response_model=ClassNoteWithTopics)
async def get_class_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClassNoteWithTopics:
    """
    Get a specific class note with extracted topics.

    - **note_id**: The class note ID
    """
    # Get class note
    result = await db.execute(
        select(ClassNote).where(
            and_(
                ClassNote.note_id == note_id,
                ClassNote.user_id == current_user.user_id,
            )
        )
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class note not found",
        )

    # Get topics
    result = await db.execute(
        select(Topic).where(Topic.note_id == note_id)
    )
    topics = result.scalars().all()

    from app.schemas.class_note import TopicResponse

    note_response = ClassNoteResponse.model_validate(note)
    topic_responses = [TopicResponse.model_validate(t) for t in topics]

    return ClassNoteWithTopics(
        **note_response.model_dump(),
        topics=topic_responses,
    )


@router.put("/{note_id}", response_model=ClassNoteResponse)
async def update_class_note(
    note_id: int,
    update_data: ClassNoteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClassNoteResponse:
    """
    Update class note title.

    - **note_id**: The class note ID
    - **title**: New title
    """
    # Get class note
    result = await db.execute(
        select(ClassNote).where(
            and_(
                ClassNote.note_id == note_id,
                ClassNote.user_id == current_user.user_id,
            )
        )
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class note not found",
        )

    # Update title if provided
    if update_data.title:
        note.title = update_data.title

    await db.flush()
    await db.refresh(note)

    return ClassNoteResponse.model_validate(note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete class note and associated topics.

    - **note_id**: The class note ID
    """
    # Get class note
    result = await db.execute(
        select(ClassNote).where(
            and_(
                ClassNote.note_id == note_id,
                ClassNote.user_id == current_user.user_id,
            )
        )
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class note not found",
        )

    # Delete file from storage
    file_storage.delete_file(note.photo_path)

    # Delete topics (cascade)
    await db.execute(
        select(Topic).where(Topic.note_id == note_id)
    )

    # Delete database record (topics will cascade)
    await db.delete(note)
