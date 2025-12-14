"""Study endpoints for flashcard and quiz generation."""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_session
from app.api.deps import get_current_user
from app.models import User, Document, Course, Enrollment
from app.schemas import FlashcardResponse, QuizResponse
from app.services.study_service import study_service

router = APIRouter()
logger = logging.getLogger(__name__)


async def verify_document_access(
    document_id: UUID,
    current_user: User,
    session: AsyncSession
) -> Document:
    """
    Verify that the current user has access to the specified document.

    Teachers must own the course, students must be enrolled.

    Args:
        document_id: The document ID to check
        current_user: The current authenticated user
        session: Database session

    Returns:
        Document object if user has access

    Raises:
        HTTPException: 404 if document not found, 403 if user lacks access
    """
    # Get document
    result = await session.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get course
    result = await session.execute(
        select(Course).where(Course.id == document.course_id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check access based on role
    if current_user.role == "teacher":
        # Teachers must own the course
        if course.teacher_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this document"
            )
    elif current_user.role == "student":
        # Students must be enrolled
        result = await session.execute(
            select(Enrollment).where(
                Enrollment.user_id == current_user.id,
                Enrollment.course_id == document.course_id
            )
        )
        enrollment = result.scalar_one_or_none()

        if not enrollment:
            raise HTTPException(
                status_code=403,
                detail="You must be enrolled in the course to access this document"
            )
    else:
        raise HTTPException(status_code=403, detail="Invalid user role")

    return document


@router.post("/documents/{document_id}/flashcards", response_model=FlashcardResponse)
async def generate_flashcards(
    document_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Generate flashcards from a document.

    Generates a fresh set of flashcards each time (stateless).
    Uses GPT-4o to extract key concepts and create study cards.

    Requirements:
    - Teachers must own the course containing the document
    - Students must be enrolled in the course
    - Document must have been processed (chunks available)

    Args:
        document_id: UUID of the document
        session: Database session
        current_user: Authenticated user

    Returns:
        FlashcardResponse with 10 generated flashcards

    Raises:
        404: Document not found
        403: User lacks access to document
        400: Document not yet processed
        500: Generation failed
    """
    # Verify user has access to this document
    await verify_document_access(document_id, current_user, session)

    # Generate flashcards
    try:
        flashcards = await study_service.generate_flashcards(
            document_id=document_id,
            session=session
        )

        logger.info(
            f"Generated {flashcards.total_cards} flashcards for document {document_id} "
            f"(user: {current_user.email})"
        )

        return flashcards

    except ValueError as e:
        # Document not found or not processed
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to generate flashcards: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate flashcards. Please try again."
        )


@router.post("/documents/{document_id}/quiz", response_model=QuizResponse)
async def generate_quiz(
    document_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Generate a multiple-choice quiz from a document.

    Generates a fresh quiz each time (stateless).
    Uses GPT-4o to create assessment questions.

    Requirements:
    - Teachers must own the course containing the document
    - Students must be enrolled in the course
    - Document must have been processed (chunks available)

    Args:
        document_id: UUID of the document
        session: Database session
        current_user: Authenticated user

    Returns:
        QuizResponse with 5 generated quiz questions

    Raises:
        404: Document not found
        403: User lacks access to document
        400: Document not yet processed
        500: Generation failed
    """
    # Verify user has access to this document
    await verify_document_access(document_id, current_user, session)

    # Generate quiz
    try:
        quiz = await study_service.generate_quiz(
            document_id=document_id,
            session=session
        )

        logger.info(
            f"Generated {quiz.total_questions} quiz questions for document {document_id} "
            f"(user: {current_user.email})"
        )

        return quiz

    except ValueError as e:
        # Document not found or not processed
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to generate quiz: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate quiz. Please try again."
        )
