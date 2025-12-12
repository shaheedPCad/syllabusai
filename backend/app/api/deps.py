from typing import Annotated
from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_session
from app.models import User


async def get_current_user(
    x_user_email: Annotated[str, Header()],
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Dev authentication: lookup user by email header.
    Header: x-user-email
    Raises 401 if user not found.
    """
    result = await session.execute(
        select(User).where(User.email == x_user_email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401,
            detail=f"User with email '{x_user_email}' not found"
        )

    return user


async def get_current_teacher(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verify current user is a teacher.
    Raises 403 if not a teacher.
    """
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can perform this action"
        )

    return current_user
