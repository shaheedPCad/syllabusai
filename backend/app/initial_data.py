#!/usr/bin/env python3
"""
Seed script for Clarity LMS development database.
Creates:
- 1 teacher (teacher@clarity.com)
- 1 student (student@clarity.com)
- 1 sample course taught by the teacher
"""
import asyncio
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session_maker
from app.models import User, Course


async def create_initial_data() -> None:
    """Create initial development data."""
    async with async_session_maker() as session:
        # Check if data already exists
        result = await session.execute(
            select(User).where(User.email == "teacher@clarity.com")
        )
        if result.scalar_one_or_none():
            print("✓ Initial data already exists. Skipping seed.")
            return

        print("Creating initial data...")

        # Create teacher
        teacher = User(
            id=uuid4(),
            email="teacher@clarity.com",
            full_name="Dr. Sarah Johnson",
            role="teacher"
        )
        session.add(teacher)

        # Create student
        student = User(
            id=uuid4(),
            email="student@clarity.com",
            full_name="Alex Smith",
            role="student"
        )
        session.add(student)

        # Flush to get teacher ID
        await session.flush()

        # Create sample course
        course = Course(
            id=uuid4(),
            title="Introduction to Computer Science",
            description="Learn the fundamentals of programming and computer science",
            course_code="CS101",
            join_code="ABC123",
            teacher_id=teacher.id
        )
        session.add(course)

        await session.commit()

        print(f"✓ Created teacher: {teacher.email}")
        print(f"✓ Created student: {student.email}")
        print(f"✓ Created course: {course.title} (join code: {course.join_code})")
        print("\nDevelopment data ready!")
        print("\nTest with:")
        print(f"  curl -H 'x-user-email: teacher@clarity.com' http://localhost:8000/api/v1/courses")


if __name__ == "__main__":
    asyncio.run(create_initial_data())
