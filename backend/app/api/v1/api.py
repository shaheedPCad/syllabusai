from fastapi import APIRouter

from app.api.v1.endpoints import courses, documents

api_router = APIRouter()
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(documents.router, tags=["documents"])
