"""
Clarity LMS - Core Module
Exports configuration and database utilities.
"""
from app.core.config import settings
from app.core.db import get_session, engine, init_db

__all__ = ["settings", "get_session", "engine", "init_db"]
