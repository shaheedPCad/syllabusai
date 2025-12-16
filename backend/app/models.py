"""
Clarity LMS - Database Models
All SQLModel ORM models with relationships and pgvector support.
"""
from datetime import datetime
from typing import Optional, List
import uuid

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, DateTime, Text, func, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from pgvector.sqlalchemy import Vector


# ============================================================================
# USER MODEL
# ============================================================================

class User(SQLModel, table=True):
    """User model for teachers and students."""

    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )
    email: str = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(max_length=255)
    role: str = Field(max_length=50)  # 'teacher' or 'student'
    profile_image: Optional[str] = Field(default=None, max_length=512)

    created_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now()
        )
    )

    # Relationships
    taught_courses: List["Course"] = Relationship(back_populates="teacher")
    enrollments: List["Enrollment"] = Relationship(back_populates="user")
    grades: List["Grade"] = Relationship(
        back_populates="student",
        sa_relationship_kwargs={"foreign_keys": "Grade.student_id"}
    )
    study_notes: List["StudyNote"] = Relationship(back_populates="user")
    flashcard_sets: List["StudyFlashcardSet"] = Relationship(back_populates="user")
    quiz_sets: List["StudyQuizSet"] = Relationship(back_populates="user")


# ============================================================================
# COURSE MODEL
# ============================================================================

class Course(SQLModel, table=True):
    """Course model for classes."""

    __tablename__ = "courses"
    __table_args__ = (
        UniqueConstraint('teacher_id', 'course_code', name='uq_courses_teacher_course_code'),
    )

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    course_code: str = Field(max_length=50, index=True)
    join_code: str = Field(unique=True, max_length=50, index=True)

    teacher_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"))
    )

    created_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now()
        )
    )

    # Relationships
    teacher: Optional[User] = Relationship(back_populates="taught_courses")
    enrollments: List["Enrollment"] = Relationship(back_populates="course")
    grades: List["Grade"] = Relationship(back_populates="course")
    documents: List["Document"] = Relationship(back_populates="course")


# ============================================================================
# ENROLLMENT MODEL
# ============================================================================

class Enrollment(SQLModel, table=True):
    """Enrollment linking students to courses."""

    __tablename__ = "enrollments"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"))
    )
    course_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("courses.id"))
    )

    enrolled_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    created_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now()
        )
    )

    # Relationships
    user: Optional[User] = Relationship(back_populates="enrollments")
    course: Optional[Course] = Relationship(back_populates="enrollments")


# ============================================================================
# GRADE MODEL
# ============================================================================

class Grade(SQLModel, table=True):
    """Grade records for students in courses."""

    __tablename__ = "grades"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    student_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"))
    )
    course_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("courses.id"))
    )

    title: str = Field(max_length=255)
    score: float = Field(ge=0)  # Greater than or equal to 0
    max_score: float = Field(gt=0)  # Greater than 0
    feedback: Optional[str] = Field(default=None, sa_column=Column(Text))

    created_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now()
        )
    )

    # Relationships
    student: Optional[User] = Relationship(
        back_populates="grades",
        sa_relationship_kwargs={"foreign_keys": "Grade.student_id"}
    )
    course: Optional[Course] = Relationship(back_populates="grades")


# ============================================================================
# DOCUMENT MODEL
# ============================================================================

class Document(SQLModel, table=True):
    """Uploaded documents (PDFs, etc.) for courses."""

    __tablename__ = "documents"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    course_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("courses.id"))
    )

    filename: str = Field(max_length=255)
    s3_key: str = Field(max_length=512)  # S3 object key
    mime_type: str = Field(max_length=100)

    created_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now()
        )
    )

    # Relationships
    course: Optional[Course] = Relationship(back_populates="documents")
    chunks: List["DocumentChunk"] = Relationship(back_populates="document")
    study_notes: List["StudyNote"] = Relationship(back_populates="document")
    flashcard_sets: List["StudyFlashcardSet"] = Relationship(back_populates="document")
    quiz_sets: List["StudyQuizSet"] = Relationship(back_populates="document")


# ============================================================================
# DOCUMENT CHUNK MODEL (with pgvector)
# ============================================================================

class DocumentChunk(SQLModel, table=True):
    """Text chunks from documents with vector embeddings for RAG."""

    __tablename__ = "document_chunks"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    document_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("documents.id"))
    )

    text_content: str = Field(sa_column=Column(Text))
    chunk_index: int = Field(ge=0)

    # pgvector column for OpenAI embeddings (1536 dimensions)
    embedding: Optional[List[float]] = Field(
        default=None,
        sa_column=Column(Vector(1536))
    )

    created_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now()
        )
    )

    # Relationships
    document: Optional[Document] = Relationship(back_populates="chunks")


# ============================================================================
# STUDY HUB MODELS
# ============================================================================

class StudyNote(SQLModel, table=True):
    """Persisted study notes (brief or thorough) generated from documents."""

    __tablename__ = "study_notes"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    document_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("documents.id"), index=True)
    )
    user_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )

    mode: str = Field(max_length=20)  # "brief" or "thorough"
    content: str = Field(sa_column=Column(Text))  # Markdown content

    created_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    # Relationships
    document: Optional[Document] = Relationship(back_populates="study_notes")
    user: Optional[User] = Relationship(back_populates="study_notes")


class StudyFlashcardSet(SQLModel, table=True):
    """Persisted flashcard sets generated from documents."""

    __tablename__ = "study_flashcard_sets"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    document_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("documents.id"), index=True)
    )
    user_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )

    flashcards: str = Field(sa_column=Column(Text))  # JSON array of Flashcard objects
    total_cards: int = Field(ge=0)

    created_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    # Relationships
    document: Optional[Document] = Relationship(back_populates="flashcard_sets")
    user: Optional[User] = Relationship(back_populates="flashcard_sets")


class StudyQuizSet(SQLModel, table=True):
    """Persisted quiz sets generated from documents."""

    __tablename__ = "study_quiz_sets"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    document_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("documents.id"), index=True)
    )
    user_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )

    questions: str = Field(sa_column=Column(Text))  # JSON array of QuizQuestion objects
    total_questions: int = Field(ge=0)

    created_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    # Relationships
    document: Optional[Document] = Relationship(back_populates="quiz_sets")
    user: Optional[User] = Relationship(back_populates="quiz_sets")
