"""AI Prompt Template routes for Kongtze API"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.models.ai_prompt_template import AIPromptTemplate
from app.models.user import User
from app.api.deps import get_current_user
from pydantic import BaseModel


# Schemas
class PromptTemplateCreate(BaseModel):
    template_name: str
    template_type: str
    prompt_template: str
    description: Optional[str] = None
    is_active: bool = True


class PromptTemplateUpdate(BaseModel):
    template_name: Optional[str] = None
    template_type: Optional[str] = None
    prompt_template: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class PromptTemplateResponse(BaseModel):
    template_id: int
    template_name: str
    template_type: str
    prompt_template: str
    description: Optional[str]
    is_active: bool
    is_system: bool

    class Config:
        from_attributes = True


router = APIRouter(prefix="/prompt-templates", tags=["Prompt Templates"])


@router.get("", response_model=List[PromptTemplateResponse])
async def get_prompt_templates(
    template_type: Optional[str] = None,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[PromptTemplateResponse]:
    """Get all prompt templates, optionally filtered by type"""
    query = select(AIPromptTemplate)

    if template_type:
        query = query.where(AIPromptTemplate.template_type == template_type)

    if active_only:
        query = query.where(AIPromptTemplate.is_active == True)

    query = query.order_by(AIPromptTemplate.template_name)

    result = await db.execute(query)
    templates = result.scalars().all()

    return [PromptTemplateResponse.model_validate(t) for t in templates]


@router.get("/{template_id}", response_model=PromptTemplateResponse)
async def get_prompt_template(
    template_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PromptTemplateResponse:
    """Get a specific prompt template by ID"""
    result = await db.execute(
        select(AIPromptTemplate).where(AIPromptTemplate.template_id == template_id)
    )
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt template not found",
        )

    return PromptTemplateResponse.model_validate(template)


@router.post("", response_model=PromptTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_prompt_template(
    template_data: PromptTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PromptTemplateResponse:
    """Create a new prompt template"""
    # Check if template name already exists
    result = await db.execute(
        select(AIPromptTemplate).where(AIPromptTemplate.template_name == template_data.template_name)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Template with this name already exists",
        )

    new_template = AIPromptTemplate(
        template_name=template_data.template_name,
        template_type=template_data.template_type,
        prompt_template=template_data.prompt_template,
        description=template_data.description,
        is_active=template_data.is_active,
        is_system=False,
    )

    db.add(new_template)
    await db.commit()
    await db.refresh(new_template)

    return PromptTemplateResponse.model_validate(new_template)


@router.put("/{template_id}", response_model=PromptTemplateResponse)
async def update_prompt_template(
    template_id: int,
    template_data: PromptTemplateUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PromptTemplateResponse:
    """Update an existing prompt template"""
    result = await db.execute(
        select(AIPromptTemplate).where(AIPromptTemplate.template_id == template_id)
    )
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt template not found",
        )

    # Update fields if provided
    if template_data.template_name is not None:
        template.template_name = template_data.template_name
    if template_data.template_type is not None:
        template.template_type = template_data.template_type
    if template_data.prompt_template is not None:
        template.prompt_template = template_data.prompt_template
    if template_data.description is not None:
        template.description = template_data.description
    if template_data.is_active is not None:
        template.is_active = template_data.is_active

    await db.commit()
    await db.refresh(template)

    return PromptTemplateResponse.model_validate(template)


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt_template(
    template_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a prompt template (only non-system templates)"""
    result = await db.execute(
        select(AIPromptTemplate).where(AIPromptTemplate.template_id == template_id)
    )
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt template not found",
        )

    if template.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete system templates",
        )

    await db.delete(template)
    await db.commit()


@router.post("/{template_id}/preview")
async def preview_prompt(
    template_id: int,
    variables: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Preview a prompt template with provided variables

    Args:
        template_id: Template ID
        variables: Dictionary of variables to substitute in the template

    Returns:
        Dictionary with the rendered prompt
    """
    result = await db.execute(
        select(AIPromptTemplate).where(AIPromptTemplate.template_id == template_id)
    )
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt template not found",
        )

    # Render the template with provided variables
    try:
        rendered_prompt = template.prompt_template.format(**variables)
        return {
            "template_id": template_id,
            "template_name": template.template_name,
            "rendered_prompt": rendered_prompt,
            "variables_used": variables
        }
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required variable: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error rendering template: {str(e)}",
        )


@router.post("/{template_id}/render-complete")
async def render_complete_prompt(
    template_id: int,
    user_id: int,
    subject_id: int,
    num_questions: int = 10,
    difficulty_level: int = 2,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Render a complete prompt with full context for test generation

    Args:
        template_id: Template ID
        user_id: User ID for context
        subject_id: Subject ID for context
        num_questions: Number of questions to generate
        difficulty_level: Difficulty level (1-4)

    Returns:
        Dictionary with the complete rendered prompt and all context used
    """
    from app.services.test_context_builder import test_context_builder
    from app.models.subject import Subject
    from app.models.student_profile import StudentProfile

    # Get template
    result = await db.execute(
        select(AIPromptTemplate).where(AIPromptTemplate.template_id == template_id)
    )
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt template not found",
        )

    # Get subject
    subject_result = await db.execute(
        select(Subject).where(Subject.subject_id == subject_id)
    )
    subject = subject_result.scalar_one_or_none()

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    # Get student profile
    profile_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == user_id)
    )
    profile = profile_result.scalar_one_or_none()

    # Build context
    context = await test_context_builder.build_context(
        user_id=user_id,
        subject_id=subject_id,
        db=db
    )

    # Prepare variables for rendering
    variables = {
        "context": context,
        "num_questions": num_questions,
        "difficulty_level": difficulty_level,
        "age": profile.age if profile else "unknown",
        "grade_level": profile.grade_level if profile else "unknown",
        "subject_name": subject.name,
        "subject_level": "unknown",
        "strengths": ", ".join(profile.strengths) if profile and profile.strengths else "none specified",
        "weaknesses": ", ".join(profile.weaknesses) if profile and profile.weaknesses else "none specified",
        "question_types": "multiple_choice, true_false, short_answer, essay"
    }

    # Determine subject level based on subject name
    if profile:
        if "math" in subject.name.lower():
            variables["subject_level"] = profile.math_level
        elif "english" in subject.name.lower():
            variables["subject_level"] = profile.english_level
        elif "chinese" in subject.name.lower():
            variables["subject_level"] = profile.chinese_level

    # Render the template
    try:
        rendered_prompt = template.prompt_template.format(**variables)
        return {
            "template_id": template_id,
            "template_name": template.template_name,
            "rendered_prompt": rendered_prompt,
            "variables_used": variables,
            "context_length": len(context),
            "estimated_tokens": len(rendered_prompt) // 4  # Rough estimate
        }
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required variable: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error rendering template: {str(e)}",
        )

