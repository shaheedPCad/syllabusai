"""
Friendship schemas for user connections.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class FriendRead(BaseModel):
    """Friend user information."""

    id: UUID
    email: str
    full_name: str
    role: str
    avatar_url: Optional[str] = None


class FriendshipRead(BaseModel):
    """Friendship with friend details."""

    id: UUID
    friend: FriendRead
    status: str
    created_at: datetime


class FriendRequestCreate(BaseModel):
    """Request to send friend request."""

    friend_email: str


class FriendRequestAccept(BaseModel):
    """Accept friend request."""

    friendship_id: UUID
