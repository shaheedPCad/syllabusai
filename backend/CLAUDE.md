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
├── app/                    # FastAPI application (to be created)
│   ├── main.py            # FastAPI app entry point
│   ├── celery_worker.py   # Celery configuration
│   ├── models/            # SQLModel database models
│   ├── api/               # API route handlers
│   ├── services/          # Business logic
│   └── core/              # Configuration and utilities
├── alembic/               # Database migrations (to be initialized)
├── rag_spike.py           # RAG prototype (spike code)
├── debug_pdf.py           # PDF debugging utility
├── Dockerfile             # Container definition
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── CLAUDE.md             # This file
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
