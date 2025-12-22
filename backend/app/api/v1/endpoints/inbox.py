"""
Inbox/messaging endpoint for user-to-user messages.
"""
from typing import List
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.db import get_session
from app.api.deps import get_current_user
from app.models import User, Message
from app.schemas import MessageCreate, MessageRead, UserBasic

router = APIRouter()


@router.post("/", response_model=MessageRead, status_code=201)
async def send_message(
    message_in: MessageCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Send a message to another user."""
    # Find recipient by email
    result = await session.execute(
        select(User).where(User.email == message_in.recipient_email)
    )
    recipient = result.scalar_one_or_none()

    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    if recipient.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send message to yourself")

    # Create message
    message = Message(
        sender_id=current_user.id,
        recipient_id=recipient.id,
        subject=message_in.subject,
        body=message_in.body,
        course_id=message_in.course_id
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)

    return MessageRead(
        id=message.id,
        sender=UserBasic(
            id=current_user.id,
            email=current_user.email,
            full_name=current_user.full_name,
            avatar_url=current_user.avatar_url
        ),
        recipient=UserBasic(
            id=recipient.id,
            email=recipient.email,
            full_name=recipient.full_name,
            avatar_url=recipient.avatar_url
        ),
        subject=message.subject,
        body=message.body,
        is_read=message.is_read,
        read_at=message.read_at,
        course_id=message.course_id,
        created_at=message.created_at
    )


@router.get("/", response_model=List[MessageRead])
async def list_messages(
    folder: str = 'inbox',  # 'inbox' or 'sent'
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get messages (inbox or sent)."""
    if folder == 'inbox':
        query = (
            select(Message)
            .options(selectinload(Message.sender), selectinload(Message.recipient))
            .where(Message.recipient_id == current_user.id)
        )
    elif folder == 'sent':
        query = (
            select(Message)
            .options(selectinload(Message.sender), selectinload(Message.recipient))
            .where(Message.sender_id == current_user.id)
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid folder parameter")

    query = query.order_by(Message.created_at.desc())
    result = await session.execute(query)
    messages = result.scalars().all()

    return [
        MessageRead(
            id=message.id,
            sender=UserBasic(
                id=message.sender.id,
                email=message.sender.email,
                full_name=message.sender.full_name,
                avatar_url=message.sender.avatar_url
            ),
            recipient=UserBasic(
                id=message.recipient.id,
                email=message.recipient.email,
                full_name=message.recipient.full_name,
                avatar_url=message.recipient.avatar_url
            ),
            subject=message.subject,
            body=message.body,
            is_read=message.is_read,
            read_at=message.read_at,
            course_id=message.course_id,
            created_at=message.created_at
        )
        for message in messages
    ]


@router.put("/{message_id}/read", status_code=200)
async def mark_as_read(
    message_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Mark message as read."""
    result = await session.execute(
        select(Message).where(
            Message.id == message_id,
            Message.recipient_id == current_user.id
        )
    )
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    if not message.is_read:
        message.is_read = True
        message.read_at = datetime.utcnow()
        await session.commit()

    return {"message": "Message marked as read"}


@router.delete("/{message_id}", status_code=204)
async def delete_message(
    message_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a message."""
    result = await session.execute(
        select(Message).where(
            Message.id == message_id
        ).where(
            (Message.sender_id == current_user.id) | (Message.recipient_id == current_user.id)
        )
    )
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    await session.delete(message)
    await session.commit()
