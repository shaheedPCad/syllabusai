"""Study schemas for flashcard and quiz generation."""
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class Flashcard(BaseModel):
    """A single flashcard with front (question) and back (answer)."""
    front: str = Field(
        ...,
        description="Question, term, or concept (front of card)",
        min_length=3,
        max_length=500
    )
    back: str = Field(
        ...,
        description="Answer, definition, or explanation (back of card)",
        min_length=3,
        max_length=1000
    )


class FlashcardSet(BaseModel):
    """Set of flashcards generated from a document. Used by instructor."""
    flashcards: List[Flashcard] = Field(
        ...,
        min_length=5,
        max_length=15,
        description="List of flashcards (5-15 cards)"
    )


class FlashcardResponse(BaseModel):
    """Response schema for flashcard generation endpoint."""
    set_id: UUID
    flashcards: List[Flashcard]
    document_id: UUID
    document_name: str
    total_cards: int
    created_at: datetime


class QuizQuestion(BaseModel):
    """A single multiple-choice quiz question."""
    question: str = Field(
        ...,
        description="The quiz question",
        min_length=10,
        max_length=500
    )
    options: List[str] = Field(
        ...,
        min_length=2,
        max_length=6,
        description="Answer options (2-6 choices)"
    )
    correct_answer_index: int = Field(
        ...,
        ge=0,
        description="Index of correct answer in options list (0-based)"
    )
    explanation: str = Field(
        ...,
        description="Explanation of why the answer is correct",
        min_length=10,
        max_length=500
    )


class QuizSet(BaseModel):
    """Set of quiz questions generated from a document. Used by instructor."""
    questions: List[QuizQuestion] = Field(
        ...,
        min_length=3,
        max_length=10,
        description="List of quiz questions (3-10 questions)"
    )


class QuizResponse(BaseModel):
    """Response schema for quiz generation endpoint."""
    set_id: UUID
    questions: List[QuizQuestion]
    document_id: UUID
    document_name: str
    total_questions: int
    created_at: datetime


# ============================================================================
# STUDY NOTE SCHEMAS
# ============================================================================

class StudyNoteRequest(BaseModel):
    """Request for generating study note."""
    mode: str = Field(
        ...,
        pattern="^(brief|thorough)$",
        description="Note generation mode: 'brief' (cheat sheet) or 'thorough' (detailed lesson)"
    )


class StudyNoteResponse(BaseModel):
    """Response for study note generation."""
    note_id: UUID
    document_id: UUID
    document_name: str
    mode: str
    content: str = Field(
        ...,
        description="Markdown-formatted study note content"
    )
    created_at: datetime


# ============================================================================
# REQUEST SCHEMAS (for configurable counts)
# ============================================================================

class FlashcardRequest(BaseModel):
    """Request for generating flashcards with configurable count."""
    count: int = Field(
        default=10,
        ge=5,
        le=20,
        description="Number of flashcards to generate (5-20)"
    )


class QuizRequest(BaseModel):
    """Request for generating quiz with configurable count."""
    count: int = Field(
        default=5,
        ge=3,
        le=15,
        description="Number of quiz questions to generate (3-15)"
    )


# ============================================================================
# STUDY HISTORY SCHEMAS
# ============================================================================

class StudyHistoryItem(BaseModel):
    """Single item in study history."""
    id: UUID
    type: str = Field(
        ...,
        description="Type of study material: 'note', 'flashcards', or 'quiz'"
    )
    mode: Optional[str] = Field(
        default=None,
        description="Note mode ('brief' or 'thorough') - only for notes"
    )
    count: Optional[int] = Field(
        default=None,
        description="Number of items - only for flashcards/quizzes"
    )
    created_at: datetime


class StudyHistoryResponse(BaseModel):
    """All study materials for a document."""
    document_id: UUID
    document_name: str
    items: List[StudyHistoryItem]
