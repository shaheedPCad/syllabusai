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

    # Dashboard extensions
    avatar_url: Optional[str] = Field(default=None, max_length=512)
    bio: Optional[str] = Field(default=None, sa_column=Column(Text))
    phone: Optional[str] = Field(default=None, max_length=20)
    timezone: Optional[str] = Field(default='UTC', max_length=50)

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

    # Dashboard relationships
    mentor_profile: Optional["MentorProfile"] = Relationship(back_populates="user")
    following_mentors: List["UserMentorFollow"] = Relationship(back_populates="user")
    lesson_progress: List["LessonProgress"] = Relationship(back_populates="user")
    tasks: List["Task"] = Relationship(back_populates="user")
    friendships: List["Friendship"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "Friendship.user_id"}
    )
    sent_messages: List["Message"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={"foreign_keys": "Message.sender_id"}
    )
    received_messages: List["Message"] = Relationship(
        back_populates="recipient",
        sa_relationship_kwargs={"foreign_keys": "Message.recipient_id"}
    )


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

    # Dashboard extensions
    thumbnail_url: Optional[str] = Field(default=None, max_length=512)
    category: Optional[str] = Field(default=None, max_length=100)  # 'FRONTEND', 'BACKEND', etc.
    level: Optional[str] = Field(default=None, max_length=20)  # 'beginner', 'intermediate', 'advanced'
    is_published: bool = Field(default=True)
    participant_count: int = Field(default=0)  # Denormalized for performance

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

    # Dashboard relationships
    lessons: List["Lesson"] = Relationship(back_populates="course")
    tasks: List["Task"] = Relationship(back_populates="course")
    messages: List["Message"] = Relationship(back_populates="course")


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


# ============================================================================
# DASHBOARD MODELS
# ============================================================================

class Friendship(SQLModel, table=True):
    """Friendship connections between users."""

    __tablename__ = "friendships"
    __table_args__ = (
        UniqueConstraint('user_id', 'friend_id', name='uq_friendships_user_friend'),
    )

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )
    friend_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )

    status: str = Field(max_length=20)  # 'pending', 'accepted', 'blocked'

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
    user: Optional[User] = Relationship(
        back_populates="friendships",
        sa_relationship_kwargs={"foreign_keys": "Friendship.user_id"}
    )
    friend: Optional[User] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Friendship.friend_id"}
    )


class MentorProfile(SQLModel, table=True):
    """Mentor profile for teachers offering mentorship."""

    __tablename__ = "mentor_profiles"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), unique=True, index=True)
    )

    expertise: str = Field(sa_column=Column(Text))  # JSON array of expertise areas
    bio: str = Field(sa_column=Column(Text))
    rating: float = Field(default=0.0)
    total_students: int = Field(default=0)
    is_verified: bool = Field(default=False)
    hourly_rate: Optional[float] = Field(default=None)

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
    user: Optional[User] = Relationship(back_populates="mentor_profile")
    followers: List["UserMentorFollow"] = Relationship(back_populates="mentor")


class UserMentorFollow(SQLModel, table=True):
    """User following a mentor."""

    __tablename__ = "user_mentor_follows"
    __table_args__ = (
        UniqueConstraint('user_id', 'mentor_id', name='uq_user_mentor_follows'),
    )

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )
    mentor_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("mentor_profiles.id"), index=True)
    )

    followed_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    # Relationships
    user: Optional[User] = Relationship(back_populates="following_mentors")
    mentor: Optional[MentorProfile] = Relationship(back_populates="followers")


class Lesson(SQLModel, table=True):
    """Lesson within a course."""

    __tablename__ = "lessons"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    course_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("courses.id"), index=True)
    )

    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    content: Optional[str] = Field(default=None, sa_column=Column(Text))  # Markdown content
    video_url: Optional[str] = Field(default=None, max_length=512)
    duration_minutes: Optional[int] = Field(default=None)
    order_index: int = Field(index=True)  # For sequencing lessons
    is_published: bool = Field(default=False)

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
    course: Optional[Course] = Relationship(back_populates="lessons")
    progress: List["LessonProgress"] = Relationship(back_populates="lesson")


class LessonProgress(SQLModel, table=True):
    """User progress tracking for lessons."""

    __tablename__ = "lesson_progress"
    __table_args__ = (
        UniqueConstraint('user_id', 'lesson_id', name='uq_lesson_progress_user_lesson'),
    )

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )
    lesson_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("lessons.id"), index=True)
    )

    status: str = Field(max_length=20)  # 'not_started', 'in_progress', 'completed'
    progress_percentage: float = Field(default=0.0, ge=0, le=100)
    time_spent_minutes: int = Field(default=0)
    last_position: Optional[str] = Field(default=None, max_length=50)  # Video timestamp
    completed_at: Optional[datetime] = Field(default=None)

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
    user: Optional[User] = Relationship(back_populates="lesson_progress")
    lesson: Optional[Lesson] = Relationship(back_populates="progress")


class Task(SQLModel, table=True):
    """User tasks and assignments."""

    __tablename__ = "tasks"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )
    course_id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("courses.id"), index=True)
    )

    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    status: str = Field(max_length=20)  # 'todo', 'in_progress', 'completed'
    priority: str = Field(max_length=20)  # 'low', 'medium', 'high'
    due_date: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)

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
    user: Optional[User] = Relationship(back_populates="tasks")
    course: Optional[Course] = Relationship(back_populates="tasks")


class Message(SQLModel, table=True):
    """Messaging system between users."""

    __tablename__ = "messages"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True)
    )

    sender_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )
    recipient_id: uuid.UUID = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )
    course_id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("courses.id"), index=True)
    )

    subject: str = Field(max_length=255)
    body: str = Field(sa_column=Column(Text))
    is_read: bool = Field(default=False)
    read_at: Optional[datetime] = Field(default=None)

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
    sender: Optional[User] = Relationship(
        back_populates="sent_messages",
        sa_relationship_kwargs={"foreign_keys": "Message.sender_id"}
    )
    recipient: Optional[User] = Relationship(
        back_populates="received_messages",
        sa_relationship_kwargs={"foreign_keys": "Message.recipient_id"}
    )
    course: Optional[Course] = Relationship(back_populates="messages")
