"""
Lesson and lesson progress schemas.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class LessonCreate(BaseModel):
    """Create a new lesson."""

    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    duration_minutes: Optional[int] = None
    order_index: int


class LessonProgressRead(BaseModel):
    """User's progress on a lesson."""

    id: UUID
    status: str
    progress_percentage: float
    time_spent_minutes: int
    last_position: Optional[str] = None
    completed_at: Optional[datetime] = None


class LessonRead(BaseModel):
    """Lesson with optional user progress."""

    id: UUID
    course_id: UUID
    title: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    order_index: int
    is_published: bool
    progress: Optional[LessonProgressRead] = None  # User's progress if available


class LessonProgressUpdate(BaseModel):
    """Update lesson progress."""

    status: str
    progress_percentage: float
    time_spent_minutes: int
    last_position: Optional[str] = None
