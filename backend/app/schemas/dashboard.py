"""
Dashboard schemas for aggregated statistics.
"""
from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from app.schemas.task import TaskRead


class CourseProgressStats(BaseModel):
    """Course progress statistics for dashboard."""

    course_id: UUID
    course_title: str
    course_code: str
    category: Optional[str] = None
    thumbnail_url: Optional[str] = None
    total_lessons: int
    completed_lessons: int
    progress_percentage: float
    participant_count: int


class DashboardStats(BaseModel):
    """Aggregated dashboard statistics."""

    total_courses: int
    total_lessons_completed: int
    total_tasks_pending: int
    unread_messages: int
    recent_courses: List[CourseProgressStats]
    upcoming_tasks: List[TaskRead]
