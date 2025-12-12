from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserRead(BaseModel):
    """User response schema."""
    id: UUID
    email: str
    full_name: str
    role: str  # 'teacher' | 'student'

    model_config = {"from_attributes": True}
