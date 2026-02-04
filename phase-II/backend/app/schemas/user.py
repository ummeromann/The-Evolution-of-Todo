from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(min_length=8, description="Password must be at least 8 characters")


class UserResponse(BaseModel):
    """Schema for user response (excludes password)."""
    id: UUID
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str
