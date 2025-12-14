"""
Study Service for generating flashcards and quizzes from documents.
Uses instructor library for structured GPT-4o outputs.
"""
import logging
from uuid import UUID
from typing import List, Tuple

import instructor
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.models import Document, DocumentChunk
from app.schemas.study import FlashcardSet, QuizSet, FlashcardResponse, QuizResponse

logger = logging.getLogger(__name__)

# Constants
MAX_CONTENT_LENGTH = 15000  # Max characters to send to GPT
FLASHCARD_COUNT = 10
QUIZ_QUESTION_COUNT = 5


class StudyService:
    """Service for generating study materials from course documents."""

    def __init__(self):
        """Initialize study service with instructor-patched OpenAI client."""
        # Create AsyncOpenAI client
        openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        # Patch with instructor for structured outputs
        self.client = instructor.apatch(openai_client)

        self.model = "gpt-4o"

    async def generate_flashcards(
        self,
        document_id: UUID,
        session: AsyncSession
    ) -> FlashcardResponse:
        """
        Generate flashcards from a document.

        Args:
            document_id: UUID of the document
            session: Async database session

        Returns:
            FlashcardResponse with generated flashcards

        Raises:
            ValueError: If document not found or has no processed chunks
            Exception: If generation fails
        """
        logger.info(f"Generating flashcards for document {document_id}")

        # Fetch document and content
        document, content = await self._get_document_content(document_id, session)

        # Generate flashcards using GPT-4o with instructor
        flashcard_set = await self._generate_flashcard_set(content, document.filename)

        logger.info(f"Generated {len(flashcard_set.flashcards)} flashcards")

        return FlashcardResponse(
            flashcards=flashcard_set.flashcards,
            document_id=document_id,
            document_name=document.filename,
            total_cards=len(flashcard_set.flashcards)
        )

    async def generate_quiz(
        self,
        document_id: UUID,
        session: AsyncSession
    ) -> QuizResponse:
        """
        Generate a multiple-choice quiz from a document.

        Args:
            document_id: UUID of the document
            session: Async database session

        Returns:
            QuizResponse with generated quiz questions

        Raises:
            ValueError: If document not found or has no processed chunks
            Exception: If generation fails
        """
        logger.info(f"Generating quiz for document {document_id}")

        # Fetch document and content
        document, content = await self._get_document_content(document_id, session)

        # Generate quiz using GPT-4o with instructor
        quiz_set = await self._generate_quiz_set(content, document.filename)

        logger.info(f"Generated {len(quiz_set.questions)} quiz questions")

        return QuizResponse(
            questions=quiz_set.questions,
            document_id=document_id,
            document_name=document.filename,
            total_questions=len(quiz_set.questions)
        )

    async def _get_document_content(
        self,
        document_id: UUID,
        session: AsyncSession
    ) -> Tuple[Document, str]:
        """
        Retrieve document and its text content from chunks.

        Args:
            document_id: UUID of the document
            session: Async database session

        Returns:
            Tuple of (Document, concatenated_text_content)

        Raises:
            ValueError: If document not found or has no chunks
        """
        # Fetch document
        result = await session.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if not document:
            raise ValueError(f"Document {document_id} not found")

        # Fetch chunks ordered by chunk_index
        result = await session.execute(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )
        chunks = result.scalars().all()

        if not chunks:
            raise ValueError(
                f"Document '{document.filename}' has not been processed yet. "
                "Please wait for processing to complete."
            )

        # Concatenate chunk text, truncate to MAX_CONTENT_LENGTH
        full_text = "\n\n".join(chunk.text_content for chunk in chunks)
        truncated_text = full_text[:MAX_CONTENT_LENGTH]

        if len(full_text) > MAX_CONTENT_LENGTH:
            logger.info(
                f"Truncated document from {len(full_text)} to {MAX_CONTENT_LENGTH} chars"
            )

        logger.info(f"Retrieved {len(chunks)} chunks, {len(truncated_text)} chars")
        return document, truncated_text

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _generate_flashcard_set(
        self,
        content: str,
        document_name: str
    ) -> FlashcardSet:
        """
        Generate flashcards using GPT-4o with instructor.

        Args:
            content: Document text content
            document_name: Name of the document (for context)

        Returns:
            FlashcardSet with generated flashcards
        """
        system_prompt = """You are an expert educator creating study flashcards.

Your task is to generate high-quality flashcards from the provided educational material.

Guidelines:
- Create exactly 10 flashcards that cover the most important concepts
- Front of card: Clear, concise question or term
- Back of card: Complete, accurate answer or definition
- Focus on key concepts, definitions, processes, and important facts
- Use clear, student-friendly language
- Ensure answers are self-contained (don't assume card order)
- Vary question types (what, why, how, define, etc.)
- Prioritize depth over breadth - cover important topics thoroughly"""

        user_prompt = f"""Document: {document_name}

Content:
{content}

Generate 10 flashcards covering the most important concepts from this material."""

        # Instructor automatically validates response against FlashcardSet schema
        flashcard_set = await self.client.chat.completions.create(
            model=self.model,
            response_model=FlashcardSet,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        return flashcard_set

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _generate_quiz_set(
        self,
        content: str,
        document_name: str
    ) -> QuizSet:
        """
        Generate quiz questions using GPT-4o with instructor.

        Args:
            content: Document text content
            document_name: Name of the document (for context)

        Returns:
            QuizSet with generated quiz questions
        """
        system_prompt = """You are an expert educator creating multiple-choice quiz questions.

Your task is to generate high-quality quiz questions from the provided educational material.

Guidelines:
- Create exactly 5 multiple-choice questions covering key concepts
- Each question should have 4 answer options
- Ensure exactly one option is correct
- Write clear, unambiguous questions
- Make distractors plausible but clearly incorrect
- Provide a concise explanation for the correct answer
- Focus on understanding, not just recall
- Vary difficulty levels (mix easy, medium, hard)
- Cover different topics from the material"""

        user_prompt = f"""Document: {document_name}

Content:
{content}

Generate 5 multiple-choice quiz questions testing understanding of this material."""

        # Instructor automatically validates response against QuizSet schema
        quiz_set = await self.client.chat.completions.create(
            model=self.model,
            response_model=QuizSet,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,  # Slightly higher for variety in distractors
            max_tokens=3000
        )

        # Validate correct_answer_index is within bounds
        for idx, question in enumerate(quiz_set.questions):
            if question.correct_answer_index >= len(question.options):
                logger.error(
                    f"Question {idx}: correct_answer_index {question.correct_answer_index} "
                    f"out of bounds for {len(question.options)} options"
                )
                raise ValueError("Generated quiz has invalid correct_answer_index")

        return quiz_set


# Singleton instance
study_service = StudyService()
