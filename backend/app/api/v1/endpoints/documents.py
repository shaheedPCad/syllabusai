"""Document upload and management endpoints."""
import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_session
from app.api.deps import get_current_user, get_current_teacher
from app.models import User, Course, Document
from app.schemas import DocumentRead
from app.services.storage import s3_service
from app.celery_worker import celery_app

logger = logging.getLogger(__name__)

router = APIRouter()


async def verify_course_teacher(
    course_id: UUID,
    current_user: User,
    session: AsyncSession
) -> Course:
    """
    Verify that the current user is the teacher of the specified course.

    Args:
        course_id: The course ID to check
        current_user: The current authenticated user
        session: Database session

    Returns:
        Course object if user is the teacher

    Raises:
        HTTPException: 404 if course not found, 403 if user is not the teacher
    """
    # Get course
    result = await session.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Verify user is a teacher
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can upload documents"
        )

    # Verify user is the teacher of this course
    if course.teacher_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not the teacher of this course"
        )

    return course


@router.post("/courses/{course_id}/documents", response_model=DocumentRead, status_code=201)
async def upload_document(
    course_id: UUID,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a document to a course (teacher only).

    Args:
        course_id: UUID of the course
        file: The file to upload
        session: Database session
        current_user: Current authenticated user

    Returns:
        Created Document object
    """
    # Verify user is the teacher of this course
    course = await verify_course_teacher(course_id, current_user, session)

    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Get content type
    content_type = file.content_type or "application/octet-stream"

    try:
        # Upload to S3
        s3_key = s3_service.upload_file(
            file_obj=file.file,
            filename=file.filename,
            content_type=content_type
        )

        # Create document record
        document = Document(
            course_id=course_id,
            filename=file.filename,
            s3_key=s3_key,
            mime_type=content_type
        )
        session.add(document)
        await session.commit()
        await session.refresh(document)

        # Trigger background processing task
        celery_app.send_task(
            "process_document",
            args=[str(document.id)]
        )
        logger.info(f"Triggered processing task for document {document.id}")

        return document

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload document: {str(e)}"
        )


@router.get("/courses/{course_id}/documents", response_model=List[DocumentRead])
async def list_documents(
    course_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List all documents for a course.

    Teacher must own the course, or student must be enrolled.

    Args:
        course_id: UUID of the course
        session: Database session
        current_user: Current authenticated user

    Returns:
        List of Document objects
    """
    # Get course
    result = await session.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Verify access (same logic as get_course endpoint)
    if current_user.role == "teacher":
        if course.teacher_id != current_user.id:
            raise HTTPException(403, "Not authorized to view this course's documents")
    else:
        # Check enrollment
        from app.models import Enrollment
        result = await session.execute(
            select(Enrollment).where(
                Enrollment.user_id == current_user.id,
                Enrollment.course_id == course_id
            )
        )
        if result.scalar_one_or_none() is None:
            raise HTTPException(403, "Not enrolled in this course")

    # Get documents
    result = await session.execute(
        select(Document).where(Document.course_id == course_id)
    )
    documents = result.scalars().all()

    return documents


@router.get("/documents/{document_id}", response_model=DocumentRead)
async def get_document(
    document_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific document by ID.

    Args:
        document_id: UUID of the document
        session: Database session
        current_user: Current authenticated user

    Returns:
        Document object
    """
    # Get document
    result = await session.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Verify access to the course
    result = await session.execute(
        select(Course).where(Course.id == document.course_id)
    )
    course = result.scalar_one_or_none()

    if current_user.role == "teacher":
        if course.teacher_id != current_user.id:
            raise HTTPException(403, "Not authorized to view this document")
    else:
        # Check enrollment
        from app.models import Enrollment
        result = await session.execute(
            select(Enrollment).where(
                Enrollment.user_id == current_user.id,
                Enrollment.course_id == document.course_id
            )
        )
        if result.scalar_one_or_none() is None:
            raise HTTPException(403, "Not enrolled in this course")

    return document


@router.delete("/documents/{document_id}", status_code=204)
async def delete_document(
    document_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_teacher)
):
    """
    Delete a document (teacher only).

    Args:
        document_id: UUID of the document
        session: Database session
        current_user: Current authenticated user (must be teacher)

    Returns:
        204 No Content on success
    """
    # Get document
    result = await session.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Verify user is the teacher of this course
    result = await session.execute(
        select(Course).where(Course.id == document.course_id)
    )
    course = result.scalar_one_or_none()

    if course.teacher_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not the teacher of this course"
        )

    # Delete from S3
    s3_service.delete_file(document.s3_key)

    # Delete from database
    await session.delete(document)
    await session.commit()

    return None
