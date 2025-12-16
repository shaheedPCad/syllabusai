"""
Cleanup duplicate courses script.

For each set of duplicate courses (same title + course_code):
- Keep the oldest course (earliest created_at)
- Move all enrollments to the keeper (avoiding duplicates)
- Move all documents to the keeper
- Delete the duplicate courses
"""
import asyncio
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import engine
from app.models import Course, Enrollment, Document


async def cleanup_duplicates():
    """Merge duplicate courses and clean up database."""
    async with AsyncSession(engine) as session:
        # Get all courses grouped by (title, course_code)
        result = await session.execute(
            select(Course).order_by(Course.title, Course.course_code, Course.created_at)
        )
        all_courses = result.scalars().all()

        # Group by (title, course_code)
        course_groups = {}
        for course in all_courses:
            key = (course.title, course.course_code)
            if key not in course_groups:
                course_groups[key] = []
            course_groups[key].append(course)

        # Process each group
        total_deleted = 0
        for (title, course_code), courses in course_groups.items():
            if len(courses) <= 1:
                continue  # No duplicates

            print(f"\n=== Processing: {title} ({course_code}) ===")
            print(f"Found {len(courses)} duplicates")

            # Keep the first (oldest) course
            keeper = courses[0]
            duplicates = courses[1:]

            print(f"Keeping: {keeper.id} (created {keeper.created_at})")
            print(f"Removing {len(duplicates)} duplicates:")

            for dup in duplicates:
                print(f"  - {dup.id} (created {dup.created_at})")

                # Move enrollments
                enroll_result = await session.execute(
                    select(Enrollment).where(Enrollment.course_id == dup.id)
                )
                enrollments = enroll_result.scalars().all()

                for enrollment in enrollments:
                    # Check if student is already enrolled in keeper
                    existing = await session.execute(
                        select(Enrollment).where(
                            Enrollment.user_id == enrollment.user_id,
                            Enrollment.course_id == keeper.id
                        )
                    )
                    if existing.scalar_one_or_none():
                        # Already enrolled, delete duplicate enrollment
                        await session.delete(enrollment)
                        print(f"    Removed duplicate enrollment for user {enrollment.user_id}")
                    else:
                        # Move enrollment to keeper
                        enrollment.course_id = keeper.id
                        print(f"    Moved enrollment for user {enrollment.user_id}")

                # Move documents
                doc_result = await session.execute(
                    select(Document).where(Document.course_id == dup.id)
                )
                documents = doc_result.scalars().all()

                for doc in documents:
                    doc.course_id = keeper.id
                    print(f"    Moved document: {doc.filename}")

                # Delete duplicate course
                await session.delete(dup)
                total_deleted += 1

        # Commit all changes
        await session.commit()

        print(f"\n✅ Cleanup complete! Deleted {total_deleted} duplicate courses")


if __name__ == "__main__":
    asyncio.run(cleanup_duplicates())
