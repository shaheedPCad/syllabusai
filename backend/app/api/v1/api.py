from fastapi import APIRouter

from app.api.v1.endpoints import courses, documents, chat, study

api_router = APIRouter()
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(documents.router, tags=["documents"])
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(study.router, tags=["study"])
