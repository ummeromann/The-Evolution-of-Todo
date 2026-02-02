from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.conversation import Conversation

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)

    # Relationship to conversations
    conversations: List["Conversation"] = Relationship(back_populates="user", cascade_delete=True)
