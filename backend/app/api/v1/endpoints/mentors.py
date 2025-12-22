"""
Mentors endpoint for managing mentor profiles and follows.
"""
from typing import List
from uuid import UUID
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.db import get_session
from app.api.deps import get_current_user
from app.models import MentorProfile, UserMentorFollow, User
from app.schemas import MentorProfileRead, UserBasic

router = APIRouter()


@router.get("/", response_model=List[MentorProfileRead])
async def list_mentors(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
):
    """List all verified mentors."""
    result = await session.execute(
        select(MentorProfile)
        .options(selectinload(MentorProfile.user))
        .where(MentorProfile.is_verified == True)
        .order_by(MentorProfile.rating.desc())
        .offset(skip)
        .limit(limit)
    )
    mentors = result.scalars().all()

    # Transform to MentorProfileRead
    mentor_reads = []
    for mentor in mentors:
        # Parse expertise JSON
        try:
            expertise_list = json.loads(mentor.expertise) if isinstance(mentor.expertise, str) else []
        except:
            expertise_list = []

        mentor_reads.append(
            MentorProfileRead(
                id=mentor.id,
                user=UserBasic(
                    id=mentor.user.id,
                    email=mentor.user.email,
                    full_name=mentor.user.full_name,
                    avatar_url=mentor.user.avatar_url
                ),
                expertise=expertise_list,
                bio=mentor.bio,
                rating=mentor.rating,
                total_students=mentor.total_students,
                is_verified=mentor.is_verified,
                hourly_rate=mentor.hourly_rate
            )
        )

    return mentor_reads


@router.get("/following", response_model=List[MentorProfileRead])
async def get_following_mentors(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get mentors followed by current user."""
    result = await session.execute(
        select(UserMentorFollow)
        .options(selectinload(UserMentorFollow.mentor).selectinload(MentorProfile.user))
        .where(UserMentorFollow.user_id == current_user.id)
    )
    follows = result.scalars().all()

    # Transform to MentorProfileRead
    mentor_reads = []
    for follow in follows:
        mentor = follow.mentor
        # Parse expertise JSON
        try:
            expertise_list = json.loads(mentor.expertise) if isinstance(mentor.expertise, str) else []
        except:
            expertise_list = []

        mentor_reads.append(
            MentorProfileRead(
                id=mentor.id,
                user=UserBasic(
                    id=mentor.user.id,
                    email=mentor.user.email,
                    full_name=mentor.user.full_name,
                    avatar_url=mentor.user.avatar_url
                ),
                expertise=expertise_list,
                bio=mentor.bio,
                rating=mentor.rating,
                total_students=mentor.total_students,
                is_verified=mentor.is_verified,
                hourly_rate=mentor.hourly_rate
            )
        )

    return mentor_reads


@router.post("/{mentor_id}/follow", status_code=201)
async def follow_mentor(
    mentor_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Follow a mentor."""
    # Verify mentor exists
    result = await session.execute(
        select(MentorProfile).where(MentorProfile.id == mentor_id)
    )
    mentor = result.scalar_one_or_none()

    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    # Check if already following
    existing = await session.execute(
        select(UserMentorFollow).where(
            UserMentorFollow.user_id == current_user.id,
            UserMentorFollow.mentor_id == mentor_id
        )
    )

    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already following this mentor")

    # Create follow relationship
    follow = UserMentorFollow(
        user_id=current_user.id,
        mentor_id=mentor_id
    )
    session.add(follow)
    await session.commit()

    return {"message": "Now following mentor"}


@router.delete("/{mentor_id}/unfollow", status_code=204)
async def unfollow_mentor(
    mentor_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Unfollow a mentor."""
    result = await session.execute(
        select(UserMentorFollow).where(
            UserMentorFollow.user_id == current_user.id,
            UserMentorFollow.mentor_id == mentor_id
        )
    )
    follow = result.scalar_one_or_none()

    if not follow:
        raise HTTPException(status_code=404, detail="Not following this mentor")

    await session.delete(follow)
    await session.commit()
