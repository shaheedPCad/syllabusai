"""Study endpoints for flashcard and quiz generation."""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_session
from app.api.deps import get_current_user
from app.models import User, Document, Course, Enrollment, StudyNote, StudyFlashcardSet, StudyQuizSet
from app.schemas import (
    FlashcardRequest,
    FlashcardResponse,
    QuizRequest,
    QuizResponse,
    StudyNoteRequest,
    StudyNoteResponse,
    StudyHistoryResponse
)
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
    request: FlashcardRequest = FlashcardRequest(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Generate and persist flashcards from a document.

    Generates flashcards with configurable count and stores them in the database.
    Uses GPT-4o to extract key concepts and create study cards.

    Requirements:
    - Teachers must own the course containing the document
    - Students must be enrolled in the course
    - Document must have been processed (chunks available)

    Args:
        document_id: UUID of the document
        request: FlashcardRequest with count (5-20, default 10)
        session: Database session
        current_user: Authenticated user

    Returns:
        FlashcardResponse with generated flashcards, set_id, and created_at

    Raises:
        404: Document not found
        403: User lacks access to document
        400: Document not yet processed
        500: Generation failed
    """
    # Verify user has access to this document
    await verify_document_access(document_id, current_user, session)

    # Generate and persist flashcards
    try:
        flashcards = await study_service.generate_flashcards(
            document_id=document_id,
            user_id=current_user.id,
            count=request.count,
            session=session
        )

        logger.info(
            f"Generated {flashcards.total_cards} flashcards for document {document_id} "
            f"(user: {current_user.email}, set_id: {flashcards.set_id})"
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
    request: QuizRequest = QuizRequest(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Generate and persist a multiple-choice quiz from a document.

    Generates quiz with configurable count and stores it in the database.
    Uses GPT-4o to create assessment questions.

    Requirements:
    - Teachers must own the course containing the document
    - Students must be enrolled in the course
    - Document must have been processed (chunks available)

    Args:
        document_id: UUID of the document
        request: QuizRequest with count (3-15, default 5)
        session: Database session
        current_user: Authenticated user

    Returns:
        QuizResponse with generated quiz questions, set_id, and created_at

    Raises:
        404: Document not found
        403: User lacks access to document
        400: Document not yet processed
        500: Generation failed
    """
    # Verify user has access to this document
    await verify_document_access(document_id, current_user, session)

    # Generate and persist quiz
    try:
        quiz = await study_service.generate_quiz(
            document_id=document_id,
            user_id=current_user.id,
            count=request.count,
            session=session
        )

        logger.info(
            f"Generated {quiz.total_questions} quiz questions for document {document_id} "
            f"(user: {current_user.email}, set_id: {quiz.set_id})"
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


@router.post("/documents/{document_id}/study-note", response_model=StudyNoteResponse)
async def generate_study_note(
    document_id: UUID,
    request: StudyNoteRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Generate and persist a study note from a document.

    Generates either a brief cheat sheet or thorough lesson and stores it in the database.
    Uses GPT-4o to summarize and structure content.

    Requirements:
    - Teachers must own the course containing the document
    - Students must be enrolled in the course
    - Document must have been processed (chunks available)

    Args:
        document_id: UUID of the document
        request: StudyNoteRequest with mode ("brief" or "thorough")
        session: Database session
        current_user: Authenticated user

    Returns:
        StudyNoteResponse with generated note, note_id, and created_at

    Raises:
        404: Document not found
        403: User lacks access to document
        400: Document not yet processed or invalid mode
        500: Generation failed
    """
    # Verify user has access to this document
    await verify_document_access(document_id, current_user, session)

    # Generate and persist study note
    try:
        note = await study_service.generate_study_note(
            document_id=document_id,
            user_id=current_user.id,
            mode=request.mode,
            session=session
        )

        logger.info(
            f"Generated {request.mode} study note for document {document_id} "
            f"(user: {current_user.email}, note_id: {note.note_id})"
        )

        return note

    except ValueError as e:
        # Document not found, not processed, or invalid mode
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to generate study note: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate study note. Please try again."
        )


@router.get("/study-notes/{note_id}", response_model=StudyNoteResponse)
async def get_study_note(
    note_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a previously generated study note.

    Requirements:
    - User must have access to the document's course

    Args:
        note_id: UUID of the study note
        session: Database session
        current_user: Authenticated user

    Returns:
        StudyNoteResponse with the note content

    Raises:
        404: Note not found
        403: User lacks access
    """
    # Fetch note
    result = await session.execute(
        select(StudyNote).where(StudyNote.id == note_id)
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Study note not found")

    # Verify user has access to this note's document
    await verify_document_access(note.document_id, current_user, session)

    # Fetch document for name
    result = await session.execute(
        select(Document).where(Document.id == note.document_id)
    )
    document = result.scalar_one_or_none()

    return StudyNoteResponse(
        note_id=note.id,
        document_id=note.document_id,
        document_name=document.filename,
        mode=note.mode,
        content=note.content,
        created_at=note.created_at
    )


@router.get("/flashcard-sets/{set_id}", response_model=FlashcardResponse)
async def get_flashcard_set(
    set_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a previously generated flashcard set.

    Requirements:
    - User must have access to the document's course

    Args:
        set_id: UUID of the flashcard set
        session: Database session
        current_user: Authenticated user

    Returns:
        FlashcardResponse with the flashcards

    Raises:
        404: Flashcard set not found
        403: User lacks access
    """
    import json
    from app.schemas.study import Flashcard

    # Fetch flashcard set
    result = await session.execute(
        select(StudyFlashcardSet).where(StudyFlashcardSet.id == set_id)
    )
    flashcard_set = result.scalar_one_or_none()

    if not flashcard_set:
        raise HTTPException(status_code=404, detail="Flashcard set not found")

    # Verify user has access to this set's document
    await verify_document_access(flashcard_set.document_id, current_user, session)

    # Fetch document for name
    result = await session.execute(
        select(Document).where(Document.id == flashcard_set.document_id)
    )
    document = result.scalar_one_or_none()

    # Deserialize flashcards from JSON
    flashcards_data = json.loads(flashcard_set.flashcards)
    flashcards = [Flashcard(**f) for f in flashcards_data]

    return FlashcardResponse(
        set_id=flashcard_set.id,
        flashcards=flashcards,
        document_id=flashcard_set.document_id,
        document_name=document.filename,
        total_cards=flashcard_set.total_cards,
        created_at=flashcard_set.created_at
    )


@router.get("/quiz-sets/{set_id}", response_model=QuizResponse)
async def get_quiz_set(
    set_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a previously generated quiz set.

    Requirements:
    - User must have access to the document's course

    Args:
        set_id: UUID of the quiz set
        session: Database session
        current_user: Authenticated user

    Returns:
        QuizResponse with the quiz questions

    Raises:
        404: Quiz set not found
        403: User lacks access
    """
    import json
    from app.schemas.study import QuizQuestion

    # Fetch quiz set
    result = await session.execute(
        select(StudyQuizSet).where(StudyQuizSet.id == set_id)
    )
    quiz_set = result.scalar_one_or_none()

    if not quiz_set:
        raise HTTPException(status_code=404, detail="Quiz set not found")

    # Verify user has access to this set's document
    await verify_document_access(quiz_set.document_id, current_user, session)

    # Fetch document for name
    result = await session.execute(
        select(Document).where(Document.id == quiz_set.document_id)
    )
    document = result.scalar_one_or_none()

    # Deserialize questions from JSON
    questions_data = json.loads(quiz_set.questions)
    questions = [QuizQuestion(**q) for q in questions_data]

    return QuizResponse(
        set_id=quiz_set.id,
        questions=questions,
        document_id=quiz_set.document_id,
        document_name=document.filename,
        total_questions=quiz_set.total_questions,
        created_at=quiz_set.created_at
    )


@router.get("/documents/{document_id}/study-history", response_model=StudyHistoryResponse)
async def get_study_history(
    document_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all study materials for a document created by the current user.

    Requirements:
    - User must have access to the document's course

    Args:
        document_id: UUID of the document
        session: Database session
        current_user: Authenticated user

    Returns:
        StudyHistoryResponse with all study materials

    Raises:
        404: Document not found
        403: User lacks access
    """
    # Verify user has access to this document
    await verify_document_access(document_id, current_user, session)

    # Get study history
    try:
        history = await study_service.get_study_history(
            document_id=document_id,
            user_id=current_user.id,
            session=session
        )

        logger.info(
            f"Retrieved {len(history.items)} study history items for document {document_id} "
            f"(user: {current_user.email})"
        )

        return history

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to retrieve study history: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve study history. Please try again."
        )
