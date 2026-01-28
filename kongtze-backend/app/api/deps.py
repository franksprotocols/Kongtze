"""Dependency injection utilities for FastAPI routes"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.schemas.user import TokenData

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify and decode token
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise credentials_exception

    # Extract user_id from token
    user_id: Optional[int] = payload.get("user_id")
    if user_id is None:
        raise credentials_exception

    # Get user from database
    result = await db.execute(
        select(User).where(User.user_id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


async def get_current_parent(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to ensure the current user is a parent.

    Raises:
        HTTPException: If user is not a parent
    """
    if not current_user.is_parent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can access this resource",
        )
    return current_user


async def get_current_student(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to ensure the current user is a student.

    Raises:
        HTTPException: If user is not a student
    """
    if current_user.is_parent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can access this resource",
        )
    return current_user
