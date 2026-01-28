"""Study session routes for Kongtze API"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.models.study_session import StudySession
from app.models.subject import Subject
from app.models.user import User
from app.schemas.study_session import (
    StudySessionCreate,
    StudySessionUpdate,
    StudySessionResponse,
)
from app.api.deps import get_current_user
from app.services.ai_service import ai_service
import json

router = APIRouter(prefix="/study-sessions", tags=["Study Sessions"])


@router.get("", response_model=List[StudySessionResponse])
async def get_study_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[StudySessionResponse]:
    """
    Get all study sessions for the current user.

    Returns the weekly calendar schedule.
    """
    result = await db.execute(
        select(StudySession)
        .where(StudySession.user_id == current_user.user_id)
        .order_by(StudySession.day_of_week, StudySession.start_time)
    )
    sessions = result.scalars().all()

    return [StudySessionResponse.model_validate(session) for session in sessions]


@router.get("/{session_id}", response_model=StudySessionResponse)
async def get_study_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StudySessionResponse:
    """
    Get a specific study session by ID.

    - **session_id**: The study session ID
    """
    result = await db.execute(
        select(StudySession).where(
            and_(
                StudySession.session_id == session_id,
                StudySession.user_id == current_user.user_id,
            )
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study session not found",
        )

    return StudySessionResponse.model_validate(session)


@router.post("", response_model=StudySessionResponse, status_code=status.HTTP_201_CREATED)
async def create_study_session(
    session_data: StudySessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StudySessionResponse:
    """
    Create a new study session.

    - **subject_id**: Subject ID (Math, English, Chinese, Science)
    - **day_of_week**: Day of week (0=Monday, 6=Sunday)
    - **start_time**: Start time (HH:MM:SS)
    - **duration_minutes**: Duration in minutes (default: 30)
    - **title**: Optional session title
    """
    # Verify subject exists
    result = await db.execute(
        select(Subject).where(Subject.subject_id == session_data.subject_id)
    )
    subject = result.scalar_one_or_none()

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    # Create new study session
    new_session = StudySession(
        user_id=current_user.user_id,
        subject_id=session_data.subject_id,
        day_of_week=session_data.day_of_week,
        start_time=session_data.start_time,
        duration_minutes=session_data.duration_minutes,
        title=session_data.title,
    )

    db.add(new_session)
    await db.flush()
    await db.refresh(new_session)

    return StudySessionResponse.model_validate(new_session)


@router.put("/{session_id}", response_model=StudySessionResponse)
async def update_study_session(
    session_id: int,
    session_data: StudySessionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StudySessionResponse:
    """
    Update an existing study session.

    - **session_id**: The study session ID
    - **subject_id**: Optional new subject ID
    - **day_of_week**: Optional new day of week
    - **start_time**: Optional new start time
    - **duration_minutes**: Optional new duration
    - **title**: Optional new title
    """
    # Get existing session
    result = await db.execute(
        select(StudySession).where(
            and_(
                StudySession.session_id == session_id,
                StudySession.user_id == current_user.user_id,
            )
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study session not found",
        )

    # Update fields if provided
    update_data = session_data.model_dump(exclude_unset=True)

    # Verify subject if being updated
    if "subject_id" in update_data:
        result = await db.execute(
            select(Subject).where(Subject.subject_id == update_data["subject_id"])
        )
        subject = result.scalar_one_or_none()

        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )

    for field, value in update_data.items():
        setattr(session, field, value)

    await db.flush()
    await db.refresh(session)

    return StudySessionResponse.model_validate(session)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_study_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete a study session.

    - **session_id**: The study session ID
    """
    # Get existing session
    result = await db.execute(
        select(StudySession).where(
            and_(
                StudySession.session_id == session_id,
                StudySession.user_id == current_user.user_id,
            )
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study session not found",
        )

    await db.delete(session)


@router.post("/generate-schedule")
async def generate_schedule(
    preferences: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Generate an optimized weekly study schedule using AI.

    - **subjects**: List of subject IDs to include
    - **subjectDifficulties**: Dict mapping subject IDs to difficulty levels
    - **hoursPerDay**: Target study hours per day (supports 0.5 increments)
    - **startTime**: Preferred start time (HH:MM)
    - **endTime**: Preferred end time (HH:MM)
    - **goals**: Study goals (optional)
    """
    # Get subject names
    result = await db.execute(select(Subject))
    all_subjects = result.scalars().all()

    selected_subjects = [
        s for s in all_subjects if s.subject_id in preferences.get("subjects", [])
    ]

    if not selected_subjects:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one subject must be selected",
        )

    # Build subject info with difficulty levels
    subject_difficulties = preferences.get("subjectDifficulties", {})
    subject_info = []
    for s in selected_subjects:
        difficulty = subject_difficulties.get(str(s.subject_id), "intermediate")
        subject_info.append(f"{s.display_name} ({difficulty} level)")

    # Build AI prompt
    prompt = f"""Generate an optimized weekly study schedule with the following requirements:

Subjects to study: {', '.join(subject_info)}
Target study hours per day: {preferences.get('hoursPerDay', 2)} hours
Time window: {preferences.get('startTime', '14:00')} to {preferences.get('endTime', '20:00')}
Goals: {preferences.get('goals', 'Balanced learning across all subjects')}

IMPORTANT CONSTRAINTS:
1. ALL sessions MUST be within the time window {preferences.get('startTime', '14:00')} to {preferences.get('endTime', '20:00')}
2. AVOID dinner time: 19:00-19:40 (7:00 PM - 7:40 PM) - do NOT schedule any sessions during this time
3. Session durations should be 30 or 45 minutes ONLY (no 60 or 90 minute sessions)
4. Maximum 3 sessions per day - NEVER schedule more than 3 sessions on any single day
5. Each subject can only appear ONCE per day - do NOT schedule the same subject twice on the same day
6. Distribute subjects evenly across the week
7. Consider each subject's difficulty level when planning
8. Include rest days (1-2 days with no or minimal study)
9. More difficult subjects may need longer or more frequent sessions

Create a balanced weekly schedule (Monday to Sunday) that respects ALL constraints above.

Return ONLY a JSON array with this exact structure (no markdown, no explanation):
[
  {{
    "day_of_week": 0,
    "subject_name": "Math",
    "start_time": "14:00:00",
    "duration_minutes": 60
  }}
]

day_of_week: 0=Monday, 1=Tuesday, ..., 6=Sunday
start_time: Must be in HH:MM:SS format and within the specified time window
duration_minutes: Must be 30 or 45 ONLY
subject_name: Must match exactly one of the subjects listed above

CRITICAL: Ensure NO sessions overlap with 19:00-19:40 (dinner time) and ALL sessions are within {preferences.get('startTime', '14:00')} to {preferences.get('endTime', '20:00')}. Maximum 3 sessions per day. Each subject appears only once per day.
"""

    # Call AI service
    try:
        ai_response = await ai_service.generate_text(prompt)

        # Parse JSON response
        # Remove markdown code blocks if present
        response_text = ai_response.strip()
        if response_text.startswith("```"):
            # Remove markdown code blocks
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1]) if len(lines) > 2 else response_text
            response_text = response_text.replace("```json", "").replace("```", "").strip()

        schedule_data = json.loads(response_text)

        # Validate schedule constraints
        validation_errors = []

        # Group sessions by day for validation
        sessions_by_day = {}
        for session in schedule_data:
            day = session.get("day_of_week")
            if day not in sessions_by_day:
                sessions_by_day[day] = []
            sessions_by_day[day].append(session)

        # Validate each day
        for day, day_sessions in sessions_by_day.items():
            # Check max 3 sessions per day
            if len(day_sessions) > 3:
                validation_errors.append(f"Day {day} has {len(day_sessions)} sessions (max 3 allowed)")

            # Check no repeated subjects per day
            subjects_seen = set()
            for session in day_sessions:
                subject = session.get("subject_name")
                if subject in subjects_seen:
                    validation_errors.append(f"Day {day} has duplicate subject: {subject}")
                subjects_seen.add(subject)

            # Check session durations
            for session in day_sessions:
                duration = session.get("duration_minutes")
                if duration not in [30, 45]:
                    validation_errors.append(f"Invalid duration {duration} minutes (must be 30 or 45)")

            # Check dinner time conflict (19:00-19:40)
            for session in day_sessions:
                start_time = session.get("start_time", "")
                duration = session.get("duration_minutes", 0)

                # Parse start time
                if start_time:
                    try:
                        time_parts = start_time.split(":")
                        if len(time_parts) < 2:
                            validation_errors.append(f"Invalid time format: {start_time}")
                            continue
                        hour, minute = int(time_parts[0]), int(time_parts[1])
                        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                            validation_errors.append(f"Invalid time values: {start_time}")
                            continue
                        start_minutes = hour * 60 + minute
                        end_minutes = start_minutes + duration

                        # Dinner time: 19:00 (1140 min) to 19:40 (1180 min)
                        dinner_start = 19 * 60  # 1140
                        dinner_end = 19 * 60 + 40  # 1180

                        # Check if session overlaps with dinner time
                        if not (end_minutes <= dinner_start or start_minutes >= dinner_end):
                            validation_errors.append(f"Session at {start_time} conflicts with dinner time (19:00-19:40)")
                    except (ValueError, IndexError) as e:
                        validation_errors.append(f"Invalid time format: {start_time}")

        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Generated schedule violates constraints: {'; '.join(validation_errors)}. Please try again.",
            )

        # Map subject names to IDs
        subject_map = {s.display_name: s.subject_id for s in all_subjects}

        # Convert to proper format
        schedule = []
        for session in schedule_data:
            subject_name = session.get("subject_name")
            subject_id = subject_map.get(subject_name)

            if subject_id:
                schedule.append({
                    "day_of_week": session["day_of_week"],
                    "subject_id": subject_id,
                    "start_time": session["start_time"],
                    "duration_minutes": session["duration_minutes"],
                })

        return {"schedule": schedule}

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse AI response: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate schedule: {str(e)}",
        )

