"""Document schemas for API request/response."""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class DocumentRead(BaseModel):
    """Document response schema."""
    id: UUID
    course_id: UUID
    filename: str
    s3_key: str
    mime_type: str
    created_at: datetime

    model_config = {"from_attributes": True}
