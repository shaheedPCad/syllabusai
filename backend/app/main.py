"""
Clarity LMS - FastAPI Application
Main application entry point with health check endpoint.
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core import settings, get_session
from app import celery_worker  # Import to ensure Celery loads


# Initialize FastAPI
app = FastAPI(
    title="Clarity LMS",
    description="Learning Management System with AI-powered features",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    """
    Health check endpoint.
    Tests database connectivity and returns status.
    """
    try:
        # Test database connection
        result = await session.execute(text("SELECT 1"))
        result.scalar_one()

        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "ok",
        "db": db_status
    }


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print(f"Starting {settings.APP_NAME}...")
    print(f"Database: {settings.DATABASE_URL.split('@')[-1]}")  # Hide credentials


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print(f"Shutting down {settings.APP_NAME}...")
