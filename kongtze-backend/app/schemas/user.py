"""User schemas for API validation"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema"""
    name: str = Field(..., min_length=1, max_length=255)


class UserCreateParent(UserBase):
    """Schema for parent user registration"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class UserCreateStudent(UserBase):
    """Schema for student user creation (by parent)"""
    pin: str = Field(..., pattern=r"^\d{4}$", description="4-digit PIN")


class UserLogin(BaseModel):
    """Schema for user login"""
    email: Optional[EmailStr] = None  # For parent login
    pin: Optional[str] = Field(None, pattern=r"^\d{4}$")  # For student login
    password: Optional[str] = None  # For parent login


class UserResponse(UserBase):
    """Schema for user response"""
    user_id: int
    email: Optional[str] = None
    is_parent: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: int
    is_parent: bool
