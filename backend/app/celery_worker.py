"""
Clarity LMS - Celery Task Queue
Handles background tasks like document processing and embeddings.
"""
from celery import Celery

from app.core.config import settings


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


# Example task (can be moved to app/tasks.py later)
@celery_app.task(name="app.celery_worker.test_task")
def test_task(message: str) -> dict:
    """Test task to verify Celery is working."""
    return {"status": "success", "message": message}
