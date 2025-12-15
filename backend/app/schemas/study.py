"""Study schemas for flashcard and quiz generation."""
from pydantic import BaseModel, Field
from typing import List
from uuid import UUID


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
    flashcards: List[Flashcard]
    document_id: UUID
    document_name: str
    total_cards: int


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
    questions: List[QuizQuestion]
    document_id: UUID
    document_name: str
    total_questions: int
