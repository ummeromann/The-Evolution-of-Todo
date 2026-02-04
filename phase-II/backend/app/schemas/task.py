from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    description: str = Field(min_length=1, max_length=500)


class TaskUpdate(BaseModel):
    """Schema for updating task description."""
    description: str = Field(min_length=1, max_length=500)


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: UUID
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskToggle(BaseModel):
    """Schema for toggle response."""
    is_completed: bool
