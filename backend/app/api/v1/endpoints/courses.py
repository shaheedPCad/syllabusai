from typing import List
from uuid import UUID
import secrets
import string

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_session
from app.api.deps import get_current_user, get_current_teacher
from app.models import User, Course, Enrollment
from app.schemas import CourseCreate, CourseRead, CourseJoin

router = APIRouter()


def generate_join_code() -> str:
    """Generate 6-character alphanumeric join code (uppercase)."""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(6))


@router.post("/", response_model=CourseRead, status_code=201)
async def create_course(
    course_in: CourseCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_teacher)
):
    """
    Create a new course (teacher only).
    Auto-generates unique join_code.
    """
    # Generate unique join code (retry if collision)
    max_retries = 5
    for _ in range(max_retries):
        join_code = generate_join_code()
        result = await session.execute(
            select(Course).where(Course.join_code == join_code)
        )
        if result.scalar_one_or_none() is None:
            break
    else:
        raise HTTPException(500, "Failed to generate unique join code")

    # Create course
    course = Course(
        title=course_in.title,
        description=course_in.description,
        course_code=course_in.course_code,
        join_code=join_code,
        teacher_id=current_user.id
    )
    session.add(course)
    await session.commit()
    await session.refresh(course)

    return course


@router.get("/", response_model=List[CourseRead])
async def list_courses(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List all courses for current user.
    Teachers: courses they teach
    Students: courses they're enrolled in
    """
    if current_user.role == "teacher":
        result = await session.execute(
            select(Course).where(Course.teacher_id == current_user.id)
        )
        courses = result.scalars().all()
    else:
        # Students: get enrolled courses
        result = await session.execute(
            select(Course)
            .join(Enrollment)
            .where(Enrollment.user_id == current_user.id)
        )
        courses = result.scalars().all()

    return courses


@router.get("/{course_id}", response_model=CourseRead)
async def get_course(
    course_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get course details by ID."""
    result = await session.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Verify access: teacher owns course OR student is enrolled
    if current_user.role == "teacher":
        if course.teacher_id != current_user.id:
            raise HTTPException(403, "Not authorized to view this course")
    else:
        result = await session.execute(
            select(Enrollment).where(
                Enrollment.user_id == current_user.id,
                Enrollment.course_id == course_id
            )
        )
        if result.scalar_one_or_none() is None:
            raise HTTPException(403, "Not enrolled in this course")

    return course


@router.post("/{course_id}/join", status_code=201)
async def join_course(
    course_id: UUID,
    join_data: CourseJoin,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Enroll student in course using join_code.
    Students only.
    """
    if current_user.role != "student":
        raise HTTPException(403, "Only students can join courses")

    # Verify course exists and join code matches
    result = await session.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(404, "Course not found")

    if course.join_code != join_data.join_code:
        raise HTTPException(403, "Invalid join code")

    # Check if already enrolled
    result = await session.execute(
        select(Enrollment).where(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(400, "Already enrolled in this course")

    # Create enrollment
    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=course_id
    )
    session.add(enrollment)
    await session.commit()

    return {"message": "Successfully enrolled in course"}
