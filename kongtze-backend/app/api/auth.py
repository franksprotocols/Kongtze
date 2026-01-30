"""Authentication routes for Kongtze API"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import (
    UserCreateParent,
    UserCreateStudent,
    UserLogin,
    UserResponse,
    Token,
)
from app.api.deps import get_current_parent, get_current_user
from app.services.student_profile_service import student_profile_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/parent", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_parent(
    user_data: UserCreateParent,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Register a new parent user.

    - **email**: Parent's email address (must be unique)
    - **password**: Parent's password (min 8 characters)
    - **name**: Parent's name
    """
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new parent user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        is_parent=True,
    )

    db.add(new_user)
    await db.flush()  # Flush to get the user_id
    await db.refresh(new_user)

    # Create access token
    access_token = create_access_token(
        data={"user_id": new_user.user_id, "is_parent": True},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token)


@router.post("/register/student", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_student(
    user_data: UserCreateStudent,
    db: AsyncSession = Depends(get_db),
    current_parent: User = Depends(get_current_parent),
) -> UserResponse:
    """
    Create a new student account (parent only).

    - **name**: Student's name
    - **pin**: 4-digit PIN for student login
    """
    # Check if PIN already exists
    result = await db.execute(
        select(User).where(User.pin == user_data.pin)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PIN already in use",
        )

    # Create new student user
    new_student = User(
        name=user_data.name,
        pin=user_data.pin,
        is_parent=False,
    )

    db.add(new_student)
    await db.flush()
    await db.refresh(new_student)

    # Create default student profile
    await student_profile_service.get_or_create_profile(
        user_id=new_student.user_id,
        db=db
    )

    return UserResponse.model_validate(new_student)


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Login for both parent and student users.

    For parent login:
    - **email**: Parent's email
    - **password**: Parent's password

    For student login:
    - **pin**: Student's 4-digit PIN
    """
    user = None

    # Parent login
    if credentials.email and credentials.password:
        result = await db.execute(
            select(User).where(User.email == credentials.email)
        )
        user = result.scalar_one_or_none()

        if not user or not user.is_parent:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

    # Student login
    elif credentials.pin:
        result = await db.execute(
            select(User).where(User.pin == credentials.pin)
        )
        user = result.scalar_one_or_none()

        if not user or user.is_parent:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid PIN",
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either email+password or PIN is required",
        )

    # Create access token
    access_token = create_access_token(
        data={"user_id": user.user_id, "is_parent": user.is_parent},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get current authenticated user information."""
    return UserResponse.model_validate(current_user)
