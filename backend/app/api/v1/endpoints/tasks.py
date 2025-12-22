"""
Tasks endpoint for managing user tasks and assignments.
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_session
from app.api.deps import get_current_user
from app.models import User, Task
from app.schemas import TaskCreate, TaskUpdate, TaskRead

router = APIRouter()


@router.post("/", response_model=TaskRead, status_code=201)
async def create_task(
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new task."""
    task = Task(
        user_id=current_user.id,
        title=task_in.title,
        description=task_in.description,
        course_id=task_in.course_id,
        status='todo',
        priority=task_in.priority,
        due_date=task_in.due_date
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        course_id=task.course_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.get("/", response_model=List[TaskRead])
async def list_tasks(
    status: Optional[str] = None,
    course_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get user's tasks with optional filters."""
    query = select(Task).where(Task.user_id == current_user.id)

    # Apply filters
    if status:
        query = query.where(Task.status == status)
    if course_id:
        query = query.where(Task.course_id == course_id)

    # Order by due date (nulls last), then priority
    query = query.order_by(
        Task.due_date.asc().nullslast(),
        Task.priority.desc()
    )

    result = await session.execute(query)
    tasks = result.scalars().all()

    return [
        TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            course_id=task.course_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update a task."""
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status
        if task_update.status == 'completed' and not task.completed_at:
            task.completed_at = datetime.utcnow()
    if task_update.priority is not None:
        task.priority = task_update.priority
    if task_update.due_date is not None:
        task.due_date = task_update.due_date

    await session.commit()
    await session.refresh(task)

    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        course_id=task.course_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a task."""
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()
