# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Clarity LMS** - A Learning Management System backend built with FastAPI, PostgreSQL (with pgvector), Redis, and Celery for background task processing. The system includes RAG (Retrieval-Augmented Generation) capabilities for processing and querying educational documents using OpenAI embeddings.

## Technology Stack

### Core Framework
- **FastAPI**: Modern async web framework
- **Uvicorn**: ASGI server with performance optimizations
- **Python 3.11**: Runtime environment

### Database & Storage
- **PostgreSQL 16 with pgvector**: Primary database with vector similarity search
- **SQLModel**: ORM built on SQLAlchemy + Pydantic
- **Alembic**: Database migrations
- **asyncpg**: Async PostgreSQL driver
- **Redis**: Cache and message broker

### Task Processing
- **Celery 5.6.0**: Distributed task queue for background jobs
- **Redis**: Celery broker and result backend

### AI & RAG
- **OpenAI API**: Embeddings (text-embedding-3-small) and chat completions (GPT-4o)
- **pgvector**: Vector similarity search in PostgreSQL
- **ChromaDB**: Optional vector database (for prototyping)
- **pypdf**: PDF text extraction
- **tiktoken**: Token counting

## Docker Infrastructure

The application runs in Docker containers orchestrated by Docker Compose.

### Services

1. **backend** (clarity_backend)
   - FastAPI application
   - Port: 8000
   - Hot reload enabled for development
   - Depends on: db, redis

2. **db** (clarity_db)
   - PostgreSQL 16 with pgvector extension
   - Port: 5432
   - Credentials: clarity_user/clarity_pass
   - Database: clarity_db
   - Persistent volume: postgres_data

3. **redis** (clarity_redis)
   - Redis Alpine
   - Port: 6379
   - Persistent volume: redis_data

4. **worker** (clarity_worker)
   - Celery worker for async task processing
   - Shares codebase with backend
   - Depends on: db, redis

### Starting the Application

```bash
# Build and start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Development Workflow

```bash
# Rebuild after dependency changes
docker-compose up --build

# Run database migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Access backend shell
docker-compose exec backend /bin/bash

# Access database
docker-compose exec db psql -U clarity_user -d clarity_db

# Monitor Celery worker
docker-compose logs -f worker
```

## Environment Setup

### Local Development (without Docker)

Python virtual environment is used for local development:

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Required environment variables (in `.env`):

```env
# Database
DATABASE_URL=postgresql+asyncpg://clarity_user:clarity_pass@db:5432/clarity_db

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-secret-key-here-please-change-in-production

# OpenAI
OPENAI_API_KEY=your-openai-api-key
```

**Note**: For local development (non-Docker), change `@db` to `@localhost` in DATABASE_URL and use `redis://localhost:6379/0` for REDIS_URL.

## Project Structure

```
backend/
├── app/                         # FastAPI application
│   ├── main.py                 # FastAPI app entry point
│   ├── celery_worker.py        # Celery configuration
│   ├── initial_data.py         # Database seed data
│   ├── models.py               # SQLModel database models (all models in one file)
│   ├── api/                    # API route handlers
│   │   ├── deps.py            # Dependencies (get_current_user, etc.)
│   │   └── v1/
│   │       ├── api.py         # API router aggregation
│   │       └── endpoints/
│   │           ├── courses.py # Course CRUD
│   │           ├── documents.py # Document upload/retrieval
│   │           ├── chat.py    # Chat with AI tutor
│   │           ├── study.py   # Flashcards, quizzes, notes
│   │           ├── friends.py # Friend management (NOT registered in router yet)
│   │           ├── inbox.py   # Messaging system (NOT registered in router yet)
│   │           ├── lessons.py # Lesson management (NOT registered in router yet)
│   │           ├── mentors.py # Mentor profiles (NOT registered in router yet)
│   │           └── tasks.py   # Task/todo management (NOT registered in router yet)
│   ├── schemas/                # Pydantic schemas for request/response
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── document.py
│   │   ├── chat.py
│   │   ├── study.py
│   │   ├── dashboard.py       # Dashboard statistics schemas
│   │   ├── friend.py          # Friend schemas
│   │   ├── inbox.py           # Message schemas
│   │   ├── lesson.py          # Lesson schemas
│   │   ├── mentor.py          # Mentor schemas
│   │   └── task.py            # Task schemas
│   ├── services/               # Business logic
│   │   ├── rag_service.py     # RAG pipeline (pgvector + OpenAI)
│   │   ├── chat_service.py    # Chat orchestration
│   │   ├── study_service.py   # Study materials generation
│   │   └── storage.py         # S3/file storage
│   └── core/                   # Configuration and utilities
│       ├── config.py          # Settings and environment variables
│       └── db.py              # Database connection and session
├── alembic/                    # Database migrations
│   └── versions/              # Migration scripts
├── rag_spike.py               # RAG prototype (spike code - reference only)
├── debug_pdf.py               # PDF debugging utility
├── docker-compose.yml         # Docker services orchestration
├── Dockerfile                 # Container definition
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── CLAUDE.md                 # This file
```

## RAG Pipeline (Prototype)

### Current Implementation (rag_spike.py)

The spike implementation demonstrates the RAG flow:

1. **PDF Text Extraction**: Uses `pypdf.PdfReader` to extract text from PDF files
2. **Text Chunking**: Splits extracted text into overlapping chunks (default: 1000 chars with 100 char overlap)
3. **Embedding Generation**: Creates embeddings using OpenAI's `text-embedding-3-small` model
4. **Vector Storage**: Stores embeddings in ChromaDB (in-memory client)
5. **Query Processing**:
   - Query text is embedded using the same model
   - ChromaDB retrieves top 10 most relevant chunks via vector similarity search
   - Retrieved context is passed to GPT-4o for answer generation

Key functions:
- `extract_text_from_pdf()`: PDF to text extraction
- `chunk_text()`: Text chunking with overlap
- `create_embeddings()`: OpenAI embedding generation
- `initialize_chromadb_and_store()`: ChromaDB setup and data ingestion
- `query_rag()`: End-to-end RAG query pipeline

**Debug Mode**: The script includes debug output that prints retrieved chunks before sending to OpenAI.

### Production RAG (To Be Implemented)

For production, RAG will use:
- **pgvector** instead of ChromaDB for vector storage
- **Celery tasks** for async PDF processing and embedding generation
- **FastAPI endpoints** for query and upload operations
- **PostgreSQL** for persistent storage of documents and embeddings

## Debug Utilities

### PDF Debug Tool

`debug_pdf.py` provides PDF text extraction verification:
- Page-by-page text extraction display
- Character counts and statistics
- Keyword search with context display

```bash
python debug_pdf.py
```

## Database Migrations

### Initial Setup

```bash
# Initialize Alembic (first time only)
docker-compose exec backend alembic init alembic

# Create first migration
docker-compose exec backend alembic revision --autogenerate -m "Initial schema"

# Apply migrations
docker-compose exec backend alembic upgrade head
```

### Working with Migrations

```bash
# Create new migration after model changes
docker-compose exec backend alembic revision --autogenerate -m "Add new table"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback one migration
docker-compose exec backend alembic downgrade -1

# View migration history
docker-compose exec backend alembic history
```

## API Development Guidelines

### FastAPI Application Structure

The FastAPI app (to be created) should follow this structure:

```python
# app/main.py
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title="Clarity LMS API")

@app.get("/")
async def root():
    return {"message": "Clarity LMS API"}
```

### Database Models

Use SQLModel for ORM models:

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
```

### Async Database Operations

Use async sessions with asyncpg:

```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(settings.DATABASE_URL)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session
```

## Celery Tasks

### Task Definition

```python
# app/celery_worker.py
from celery import Celery

celery_app = Celery(
    "clarity",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery_app.task
def process_document(document_id: int):
    # Background processing logic
    pass
```

## Key Implementation Details

### RAG Prototype (Current)
- **ChromaDB Collection**: Created fresh each run with name "resume_test" (in-memory, no persistence)
- **Embedding Model**: `text-embedding-3-small` for both document chunks and queries
- **Chat Model**: `gpt-4o` with temperature 0.7
- **Context Window**: Top 10 chunks retrieved per query
- **Chunking Strategy**: Fixed-size chunks with overlap to preserve context across boundaries

### Production Considerations
- Use pgvector for persistent vector storage
- Implement async endpoints for all database operations
- Use Celery for CPU-intensive tasks (PDF processing, embeddings)
- Implement proper error handling and logging
- Add authentication and authorization
- Use connection pooling for database connections
- Implement rate limiting for API endpoints

## pgvector Similarity Search

The application uses pgvector for semantic search over document embeddings.

### Operators

pgvector provides several distance operators for nearest neighbor queries:

| Operator | Distance Metric | SQLAlchemy Method | Use Case |
|----------|-----------------|-------------------|----------|
| `<->` | L2 (Euclidean) | `.l2_distance()` | Default distance |
| `<=>` | Cosine distance | `.cosine_distance()` | **Recommended for embeddings** |
| `<#>` | Negative inner product | `.max_inner_product()` | Normalized vectors |

### Similarity Search Pattern

The Chat API uses pgvector for semantic document retrieval:

```python
from sqlalchemy import select

# Cosine similarity (0-1, higher = more similar)
similarity = (1 - DocumentChunk.embedding.cosine_distance(query_embedding)).label("similarity")

result = await session.execute(
    select(DocumentChunk, similarity)
    .join(Document)
    .where(Document.course_id == course_id)
    .where(similarity >= 0.7)  # Threshold filter
    .order_by(similarity.desc())  # Most similar first
    .limit(5)
)

chunks_with_scores = result.all()
```

### Key Points
- Use **cosine distance** for OpenAI embeddings (normalized)
- Always use `ORDER BY` and `LIMIT` for nearest neighbor queries
- Convert distance to similarity: `similarity = 1 - distance`
- Filter by similarity threshold to exclude irrelevant results
- Join with Document table to filter by course_id

### Implemented RAG Pipeline
1. **Document Upload** → Triggers background processing (Celery)
2. **PDF Processing** → Extract text with pypdf
3. **Text Chunking** → RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
4. **Embedding Generation** → OpenAI text-embedding-3-small (1536 dimensions)
5. **Storage** → DocumentChunk table with pgvector embeddings
6. **Query** → Chat endpoint embeds question → pgvector search → GPT-4 synthesis

### Resources
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [pgvector-python SQLAlchemy Integration](https://github.com/pgvector/pgvector-python)

## API Endpoints

### Currently Active Endpoints (Registered in api.py)

All endpoints are prefixed with `/api/v1`

#### Courses (`/courses`)
- `GET /courses` - Get all courses for current user (teachers: created, students: enrolled)
- `POST /courses` - Create new course (teachers only)
- `GET /courses/{course_id}` - Get specific course details
- `POST /courses/join` - Join course by join code (students only)

#### Documents (`/courses/{course_id}/documents`)
- `GET /courses/{course_id}/documents` - Get all documents for a course
- `POST /courses/{course_id}/documents` - Upload document (triggers background processing)

#### Chat (`/courses/{course_id}/chat`)
- `POST /courses/{course_id}/chat` - Send message to AI tutor, get RAG-enhanced response

#### Study (`/courses/{course_id}/study`)
- `GET /courses/{course_id}/study/flashcards` - Get flashcard deck
- `POST /courses/{course_id}/study/flashcards/generate` - Generate new flashcards
- `GET /courses/{course_id}/study/quiz` - Get quiz
- `POST /courses/{course_id}/study/quiz/generate` - Generate new quiz
- `GET /courses/{course_id}/study/notes` - Get study notes
- `POST /courses/{course_id}/study/notes/generate` - Generate new notes

### New Endpoints (Created but NOT Yet Registered)

The following endpoints have been implemented but are **not yet included in `api.py`**. To activate them, add them to `app/api/v1/api.py`:

```python
# In app/api/v1/api.py
from app.api.v1.endpoints import courses, documents, chat, study, friends, inbox, lessons, mentors, tasks

api_router.include_router(friends.router, prefix="/friends", tags=["friends"])
api_router.include_router(inbox.router, prefix="/inbox", tags=["inbox"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
api_router.include_router(mentors.router, prefix="/mentors", tags=["mentors"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
```

#### Friends (`/friends`) - NOT REGISTERED
- `GET /friends` - Get user's accepted friendships
- `POST /friends` - Send friend request to another user
- `PUT /friends/{friendship_id}/accept` - Accept pending friend request
- `DELETE /friends/{friendship_id}` - Remove friend or reject request

#### Inbox (`/inbox`) - NOT REGISTERED
- `GET /inbox` - Get user's messages (sent and received)
- `POST /inbox` - Send message to another user
- `PUT /inbox/{message_id}/read` - Mark message as read
- `DELETE /inbox/{message_id}` - Delete message

#### Lessons (`/lessons`) - NOT REGISTERED
- `GET /courses/{course_id}/lessons` - Get all lessons for a course
- `POST /courses/{course_id}/lessons` - Create new lesson (teachers only)
- `GET /lessons/{lesson_id}` - Get specific lesson details
- `PUT /lessons/{lesson_id}` - Update lesson (teachers only)
- `DELETE /lessons/{lesson_id}` - Delete lesson (teachers only)
- `GET /lessons/{lesson_id}/progress` - Get user's progress for lesson
- `PUT /lessons/{lesson_id}/progress` - Update user's progress for lesson

#### Mentors (`/mentors`) - NOT REGISTERED
- `GET /mentors` - Get all mentor profiles
- `POST /mentors` - Create mentor profile (teachers only)
- `GET /mentors/{mentor_id}` - Get specific mentor profile
- `POST /mentors/{mentor_id}/follow` - Follow a mentor
- `DELETE /mentors/{mentor_id}/follow` - Unfollow a mentor

#### Tasks (`/tasks`) - NOT REGISTERED
- `GET /tasks` - Get user's tasks
- `POST /tasks` - Create new task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task
- `PUT /tasks/{task_id}/complete` - Mark task as complete

## Database Models

### Core Models (Implemented)

**User** (`users` table)
- Authentication and profile information
- Roles: `teacher` or `student`
- Dashboard extensions: avatar, bio, phone, timezone
- Relationships: courses, enrollments, grades, study materials, friends, messages, tasks

**Course** (`courses` table)
- Course information: title, description, course_code
- Join code for student enrollment (6-character alphanumeric)
- Dashboard extensions: category, thumbnail_url, is_published
- Relationships: teacher, students (via Enrollment), documents, grades, lessons, flashcards, quizzes, notes

**Enrollment** (`enrollments` table)
- Junction table for User ↔ Course many-to-many
- Tracks student enrollment in courses
- Unique constraint on (user_id, course_id)

**Document** (`documents` table)
- Uploaded course materials (PDFs, etc.)
- S3 storage: s3_key, filename, mime_type
- Processing status: `pending`, `processing`, `completed`, `failed`
- Celery task ID for background processing
- Relationships: course, chunks (for RAG)

**DocumentChunk** (`document_chunks` table)
- Text chunks extracted from documents
- pgvector embedding (1536 dimensions)
- Chunk metadata: sequence number, char count, token count
- Used for RAG similarity search

**Grade** (`grades` table)
- Student grades for assignments/tests
- Score, max_score, feedback
- Relationships: student, course

### Study Models (Implemented)

**StudyFlashcardSet** (`study_flashcard_sets` table)
- Generated flashcard decks for courses
- JSON array of flashcard objects: `[{"term": "...", "definition": "..."}]`
- Timestamps: created_at, updated_at

**StudyQuizSet** (`study_quiz_sets` table)
- Generated quiz sets for courses
- JSON array of quiz questions with multiple choice options
- Timestamps: created_at, updated_at

**StudyNote** (`study_notes` table)
- AI-generated study notes for courses
- Markdown content
- Timestamps: created_at, updated_at

### Dashboard Models (Implemented)

**MentorProfile** (`mentor_profiles` table)
- Teacher profiles with expertise, availability, bio
- Hourly rate (optional)
- Relationships: user, followers (students who follow this mentor)

**UserMentorFollow** (`user_mentor_follows` table)
- Junction table for User ↔ MentorProfile following
- Tracks which students follow which mentors

**Lesson** (`lessons` table)
- Course lessons with content, video_url, duration
- Order index for sequencing
- Published status
- Relationships: course, progress

**LessonProgress** (`lesson_progress` table)
- User progress tracking for lessons
- Status: `not_started`, `in_progress`, `completed`
- Progress percentage, time spent, last position (video timestamp)
- Unique constraint on (user_id, lesson_id)

**Task** (`tasks` table)
- User tasks/todos with due dates
- Priority levels
- Status: `pending`, `in_progress`, `completed`
- Course association (optional)

**Friendship** (`friendships` table)
- Friend relationships between users
- Status: `pending`, `accepted`, `blocked`
- Bidirectional relationship (user_id ↔ friend_id)

**Message** (`messages` table)
- Direct messages between users
- Subject, content, read status
- Relationships: sender, recipient

## Authentication & Authorization

### Dev Auth System

The backend uses a **development authentication** system for rapid prototyping. This should be replaced with proper JWT authentication in production.

**How it works:**
- Frontend sends `x-user-email` header with every request
- Backend dependency `get_current_user()` (in `app/api/deps.py`) looks up the user by email
- No password verification in development mode

**Example:**
```python
# app/api/deps.py
async def get_current_user(
    x_user_email: str = Header(...),
    session: AsyncSession = Depends(get_session)
) -> User:
    """Get current user from x-user-email header."""
    result = await session.execute(
        select(User).where(User.email == x_user_email)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

**Testing different roles:**
- Teacher: `x-user-email: teacher@clarity.com`
- Student: `x-user-email: student@clarity.com`
- Different student: `x-user-email: alice@clarity.com`

### Authorization Patterns

**Teacher-only endpoints:**
```python
@router.post("/courses")
async def create_course(
    course_data: CreateCourseRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create courses")
    # ...
```

**Course enrollment check:**
```python
async def get_user_course(
    course_id: UUID,
    current_user: User,
    session: AsyncSession
) -> Course:
    """Verify user has access to course (teacher or enrolled student)."""
    result = await session.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check access
    if current_user.role == "teacher" and course.teacher_id == current_user.id:
        return course  # Teacher owns course

    # Check student enrollment
    enrollment = await session.execute(
        select(Enrollment).where(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id
        )
    )
    if enrollment.scalar_one_or_none():
        return course

    raise HTTPException(status_code=403, detail="Not enrolled in this course")
```

## Testing

```bash
# Run tests (when implemented)
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app
```

## Common Issues

### Database Connection
If backend can't connect to database, ensure:
- Database service is healthy: `docker-compose ps`
- Environment variables are correct in `.env`
- Database is ready: `docker-compose logs db`

### Celery Worker Not Processing
Check worker logs:
```bash
docker-compose logs -f worker
```

Ensure Redis is running:
```bash
docker-compose exec redis redis-cli ping
```

### Hot Reload Not Working
Volume mounts enable hot reload. If changes aren't reflected:
```bash
docker-compose restart backend
```
