"""
Friends endpoint for managing user friendships.
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.core.db import get_session
from app.api.deps import get_current_user
from app.models import User, Friendship
from app.schemas import FriendRead, FriendshipRead, FriendRequestCreate

router = APIRouter()


@router.get("/", response_model=List[FriendshipRead])
async def get_friends(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get user's accepted friendships."""
    result = await session.execute(
        select(Friendship)
        .where(
            or_(
                Friendship.user_id == current_user.id,
                Friendship.friend_id == current_user.id
            ),
            Friendship.status == 'accepted'
        )
    )
    friendships = result.scalars().all()

    # Transform to FriendshipRead with friend details
    friendship_reads = []
    for friendship in friendships:
        # Determine which user is the friend
        friend_id = friendship.friend_id if friendship.user_id == current_user.id else friendship.user_id

        # Fetch friend user
        friend_result = await session.execute(
            select(User).where(User.id == friend_id)
        )
        friend = friend_result.scalar_one_or_none()

        if friend:
            friendship_reads.append(
                FriendshipRead(
                    id=friendship.id,
                    friend=FriendRead(
                        id=friend.id,
                        email=friend.email,
                        full_name=friend.full_name,
                        role=friend.role,
                        avatar_url=friend.avatar_url
                    ),
                    status=friendship.status,
                    created_at=friendship.created_at
                )
            )

    return friendship_reads


@router.post("/", status_code=201)
async def send_friend_request(
    request: FriendRequestCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Send friend request to another user."""
    # Find friend by email
    result = await session.execute(
        select(User).where(User.email == request.friend_email)
    )
    friend = result.scalar_one_or_none()

    if not friend:
        raise HTTPException(status_code=404, detail="User not found")

    if friend.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send friend request to yourself")

    # Check for existing friendship
    existing = await session.execute(
        select(Friendship).where(
            or_(
                (Friendship.user_id == current_user.id) & (Friendship.friend_id == friend.id),
                (Friendship.user_id == friend.id) & (Friendship.friend_id == current_user.id)
            )
        )
    )

    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Friendship already exists")

    # Create friendship
    friendship = Friendship(
        user_id=current_user.id,
        friend_id=friend.id,
        status='pending'
    )
    session.add(friendship)
    await session.commit()

    return {"message": "Friend request sent"}


@router.put("/{friendship_id}/accept", status_code=200)
async def accept_friend_request(
    friendship_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Accept pending friend request."""
    result = await session.execute(
        select(Friendship).where(Friendship.id == friendship_id)
    )
    friendship = result.scalar_one_or_none()

    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")

    # Verify current user is the recipient
    if friendship.friend_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to accept this request")

    if friendship.status != 'pending':
        raise HTTPException(status_code=400, detail="Friendship request is not pending")

    friendship.status = 'accepted'
    await session.commit()

    return {"message": "Friend request accepted"}


@router.delete("/{friendship_id}", status_code=204)
async def remove_friend(
    friendship_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Remove friend or reject request."""
    result = await session.execute(
        select(Friendship).where(Friendship.id == friendship_id)
    )
    friendship = result.scalar_one_or_none()

    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")

    # Verify current user is part of the friendship
    if friendship.user_id != current_user.id and friendship.friend_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    await session.delete(friendship)
    await session.commit()
