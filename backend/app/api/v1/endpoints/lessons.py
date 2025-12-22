"""
Lessons endpoint for managing course lessons and progress.
"""
from typing import List
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.db import get_session
from app.api.deps import get_current_user, get_current_teacher
from app.models import User, Course, Lesson, LessonProgress, Enrollment
from app.schemas import LessonCreate, LessonRead, LessonProgressRead, LessonProgressUpdate

router = APIRouter()


@router.post("/courses/{course_id}/lessons", response_model=LessonRead, status_code=201)
async def create_lesson(
    course_id: UUID,
    lesson_in: LessonCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_teacher)
):
    """Create lesson (teachers only)."""
    # Verify teacher owns course
    result = await session.execute(
        select(Course).where(
            Course.id == course_id,
            Course.teacher_id == current_user.id
        )
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not owned by you")

    # Create lesson
    lesson = Lesson(
        course_id=course_id,
        title=lesson_in.title,
        description=lesson_in.description,
        content=lesson_in.content,
        video_url=lesson_in.video_url,
        duration_minutes=lesson_in.duration_minutes,
        order_index=lesson_in.order_index
    )
    session.add(lesson)
    await session.commit()
    await session.refresh(lesson)

    return LessonRead(
        id=lesson.id,
        course_id=lesson.course_id,
        title=lesson.title,
        description=lesson.description,
        duration_minutes=lesson.duration_minutes,
        order_index=lesson.order_index,
        is_published=lesson.is_published,
        progress=None
    )


@router.get("/courses/{course_id}/lessons", response_model=List[LessonRead])
async def list_lessons(
    course_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get all lessons for a course with user's progress."""
    # Verify user has access to course (either teacher or enrolled student)
    is_teacher = await session.execute(
        select(Course).where(
            Course.id == course_id,
            Course.teacher_id == current_user.id
        )
    )

    is_enrolled = await session.execute(
        select(Enrollment).where(
            Enrollment.course_id == course_id,
            Enrollment.user_id == current_user.id
        )
    )

    if not is_teacher.scalar_one_or_none() and not is_enrolled.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not authorized to access this course")

    # Get all lessons
    result = await session.execute(
        select(Lesson)
        .where(Lesson.course_id == course_id)
        .order_by(Lesson.order_index)
    )
    lessons = result.scalars().all()

    # Get user's progress for all lessons
    progress_result = await session.execute(
        select(LessonProgress)
        .where(
            LessonProgress.user_id == current_user.id,
            LessonProgress.lesson_id.in_([lesson.id for lesson in lessons])
        )
    )
    progress_map = {p.lesson_id: p for p in progress_result.scalars().all()}

    # Transform to LessonRead with progress
    lesson_reads = []
    for lesson in lessons:
        progress = progress_map.get(lesson.id)
        progress_read = None
        if progress:
            progress_read = LessonProgressRead(
                id=progress.id,
                status=progress.status,
                progress_percentage=progress.progress_percentage,
                time_spent_minutes=progress.time_spent_minutes,
                last_position=progress.last_position,
                completed_at=progress.completed_at
            )

        lesson_reads.append(
            LessonRead(
                id=lesson.id,
                course_id=lesson.course_id,
                title=lesson.title,
                description=lesson.description,
                duration_minutes=lesson.duration_minutes,
                order_index=lesson.order_index,
                is_published=lesson.is_published,
                progress=progress_read
            )
        )

    return lesson_reads


@router.put("/lessons/{lesson_id}/progress", status_code=200)
async def update_lesson_progress(
    lesson_id: UUID,
    progress_data: LessonProgressUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update user's progress on a lesson."""
    # Verify lesson exists
    lesson_result = await session.execute(
        select(Lesson).where(Lesson.id == lesson_id)
    )
    lesson = lesson_result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Get or create progress record
    progress_result = await session.execute(
        select(LessonProgress).where(
            LessonProgress.user_id == current_user.id,
            LessonProgress.lesson_id == lesson_id
        )
    )
    progress = progress_result.scalar_one_or_none()

    if progress:
        # Update existing progress
        progress.status = progress_data.status
        progress.progress_percentage = progress_data.progress_percentage
        progress.time_spent_minutes = progress_data.time_spent_minutes
        progress.last_position = progress_data.last_position

        if progress_data.status == 'completed' and not progress.completed_at:
            progress.completed_at = datetime.utcnow()
    else:
        # Create new progress record
        progress = LessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            status=progress_data.status,
            progress_percentage=progress_data.progress_percentage,
            time_spent_minutes=progress_data.time_spent_minutes,
            last_position=progress_data.last_position,
            completed_at=datetime.utcnow() if progress_data.status == 'completed' else None
        )
        session.add(progress)

    await session.commit()

    return {"message": "Progress updated successfully"}
