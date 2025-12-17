"""
Messaging/inbox schemas.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserBasic(BaseModel):
    """Basic user information."""

    id: UUID
    email: str
    full_name: str
    avatar_url: Optional[str] = None


class MessageCreate(BaseModel):
    """Create a new message."""

    recipient_email: str
    subject: str
    body: str
    course_id: Optional[UUID] = None


class MessageRead(BaseModel):
    """Message with sender and recipient details."""

    id: UUID
    sender: UserBasic
    recipient: UserBasic
    subject: str
    body: str
    is_read: bool
    read_at: Optional[datetime] = None
    course_id: Optional[UUID] = None
    created_at: datetime
