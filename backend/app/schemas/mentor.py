"""
Mentor profile schemas.
"""
from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List


class UserBasic(BaseModel):
    """Basic user information."""

    id: UUID
    email: str
    full_name: str
    avatar_url: Optional[str] = None


class MentorProfileRead(BaseModel):
    """Mentor profile with details."""

    id: UUID
    user: UserBasic
    expertise: List[str]
    bio: str
    rating: float
    total_students: int
    is_verified: bool
    hourly_rate: Optional[float] = None


class MentorFollowCreate(BaseModel):
    """Follow a mentor."""

    mentor_id: UUID
