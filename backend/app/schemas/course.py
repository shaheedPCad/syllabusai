from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class CourseCreate(BaseModel):
    """Course creation request."""
    title: str
    description: Optional[str] = None
    course_code: str


class CourseRead(BaseModel):
    """Course response schema."""
    id: UUID
    title: str
    description: Optional[str]
    course_code: str
    join_code: str
    teacher_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class CourseJoin(BaseModel):
    """Enrollment via join code request."""
    join_code: str
