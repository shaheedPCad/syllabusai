"""Chat endpoint for RAG-based Q&A with course materials."""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_session
from app.api.deps import get_current_user
from app.models import User, Enrollment, Course
from app.schemas import ChatRequest, ChatResponse, DocumentSource
from app.services.chat_service import chat_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/courses/{course_id}/chat", response_model=ChatResponse)
async def chat_with_course(
    course_id: UUID,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Ask a question about course materials.

    Students must be enrolled in the course to ask questions.
    Answers are generated using RAG (Retrieval-Augmented Generation)
    from processed course documents.

    Args:
        course_id: UUID of the course
        request: ChatRequest with question
        session: Database session
        current_user: Authenticated user

    Returns:
        ChatResponse with answer and sources

    Raises:
        404: Course not found
        403: User not enrolled in course
        400: No course materials available or question processing failed
    """
    # Verify course exists
    result = await session.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if user is enrolled (students) or is the teacher
    if current_user.role == "student":
        # Students must be enrolled
        result = await session.execute(
            select(Enrollment).where(
                Enrollment.user_id == current_user.id,
                Enrollment.course_id == course_id
            )
        )
        enrollment = result.scalar_one_or_none()

        if not enrollment:
            raise HTTPException(
                status_code=403,
                detail="You must be enrolled in this course to ask questions"
            )
    elif current_user.role == "teacher":
        # Teachers must own the course
        if course.teacher_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only access your own courses"
            )
    else:
        raise HTTPException(status_code=403, detail="Invalid user role")

    # Generate answer using ChatService
    try:
        answer, chunks_with_scores = await chat_service.ask_question(
            course_id=course_id,
            question=request.question,
            session=session,
            top_k=5,
            similarity_threshold=0.5  # Lowered from 0.7 based on testing
        )

        # Build response with sources
        sources = [
            DocumentSource(
                chunk_id=str(chunk.id),
                text=chunk.text_content[:200] + "..." if len(chunk.text_content) > 200 else chunk.text_content,
                similarity_score=round(score, 3)
            )
            for chunk, score in chunks_with_scores
        ]

        # Determine confidence based on top similarity score
        max_score = max(score for _, score in chunks_with_scores)
        if max_score >= 0.75:
            confidence = "high"
        elif max_score >= 0.6:
            confidence = "medium"
        else:
            confidence = "low"

        logger.info(f"Answered question for user {current_user.email} in course {course_id}")

        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=confidence
        )

    except ValueError as e:
        # No relevant documents found
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to generate answer: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process your question. Please try again."
        )
