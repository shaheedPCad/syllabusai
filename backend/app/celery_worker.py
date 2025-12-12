"""
Clarity LMS - Celery Task Queue
Handles background tasks like document processing and embeddings.
"""
import logging
from uuid import UUID

from celery import Celery
from sqlmodel import Session, create_engine

from app.core.config import settings
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)


# Initialize Celery app
celery_app = Celery(
    "clarity",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes max
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
)

# Auto-discover tasks (will add task modules later)
# celery_app.autodiscover_tasks(['app.tasks'])

# Create synchronous engine for Celery tasks
# Convert async URL to sync URL (replace asyncpg with psycopg2)
sync_db_url = settings.DATABASE_URL.replace(
    "postgresql+asyncpg://",
    "postgresql+psycopg2://"
)
sync_engine = create_engine(sync_db_url, echo=settings.DEBUG)


# Example task (can be moved to app/tasks.py later)
@celery_app.task(name="app.celery_worker.test_task")
def test_task(message: str) -> dict:
    """Test task to verify Celery is working."""
    return {"status": "success", "message": message}


@celery_app.task(name="process_document", bind=True)
def process_document(self, document_id: str):
    """
    Background task to process document into vector embeddings.

    Args:
        document_id: UUID of document as string

    Returns:
        Dict with status and chunk count
    """
    import asyncio

    logger.info(f"Starting document processing for {document_id}")

    try:
        # Convert string to UUID
        doc_uuid = UUID(document_id)

        # Create synchronous database session
        with Session(sync_engine) as session:
            # Run async process_document in event loop
            # Celery tasks are synchronous but RAGService uses async OpenAI
            loop = asyncio.get_event_loop()
            chunk_count = loop.run_until_complete(
                rag_service.process_document(doc_uuid, session)
            )

            logger.info(f"Successfully processed document {document_id}: {chunk_count} chunks")
            return {
                "status": "success",
                "document_id": document_id,
                "chunk_count": chunk_count
            }

    except Exception as e:
        logger.error(f"Failed to process document {document_id}: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)
