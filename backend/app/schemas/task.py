"""
Task schemas for user tasks and assignments.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    """Create a new task."""

    title: str
    description: Optional[str] = None
    course_id: Optional[UUID] = None
    priority: str = 'medium'
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    """Update an existing task."""

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskRead(BaseModel):
    """Task with full details."""

    id: UUID
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    due_date: Optional[datetime] = None
    course_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
