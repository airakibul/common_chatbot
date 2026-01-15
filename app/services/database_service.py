from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.database_models import Thread, ChatMessage
from datetime import datetime
import uuid


class DatabaseService:
    
    @staticmethod
    async def create_thread(db: AsyncSession, user_id: str, thread_id: str = None):
        """Create a new thread asynchronously"""
        if not thread_id:
            thread_id = f"thread_{uuid.uuid4().hex[:8]}"
        
        thread = Thread(thread_id=thread_id, user_id=user_id)
        db.add(thread)
        await db.commit()
        await db.refresh(thread)
        return thread
    
    @staticmethod
    async def get_thread(db: AsyncSession, thread_id: str):
        """Get a thread by ID asynchronously"""
        result = await db.execute(
            select(Thread).filter(Thread.thread_id == thread_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_or_create_thread(db: AsyncSession, user_id: str, thread_id: str = None):
        """Get existing thread or create new one asynchronously"""
        if thread_id:
            result = await db.execute(
                select(Thread).filter(Thread.thread_id == thread_id)
            )
            thread = result.scalar_one_or_none()
            if thread:
                return thread
        
        return await DatabaseService.create_thread(db, user_id, thread_id)
    
    @staticmethod
    async def save_message(db: AsyncSession, thread_id: str, user_id: str, role: str, content: str):
        """Save a chat message asynchronously"""
        message = ChatMessage(
            id=f"msg_{uuid.uuid4().hex[:12]}",
            thread_id=thread_id,
            user_id=user_id,
            role=role,
            content=content
        )
        db.add(message)
        
        # Update thread's updated_at timestamp
        result = await db.execute(
            select(Thread).filter(Thread.thread_id == thread_id)
        )
        thread = result.scalar_one_or_none()
        if thread:
            thread.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(message)
        print(f"✅ SAVED to PostgreSQL: {role} message for user {user_id} in thread {thread_id}")
        return message
    
    @staticmethod
    async def get_thread_messages(db: AsyncSession, thread_id: str):
        """Get all messages in a thread asynchronously"""
        result = await db.execute(
            select(ChatMessage)
            .filter(ChatMessage.thread_id == thread_id)
            .order_by(ChatMessage.created_at)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_user_threads(db: AsyncSession, user_id: str):
        """Get all threads for a user asynchronously"""
        result = await db.execute(
            select(Thread)
            .filter(Thread.user_id == user_id)
            .order_by(Thread.updated_at.desc())
        )
        return result.scalars().all()
