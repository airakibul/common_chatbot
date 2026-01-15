from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.database import get_db
from app.services.database_service import DatabaseService
from app.schemas.chat_schemas import ThreadCreateRequest, UserThreadsRequest

router = APIRouter()

@router.post("/chat-thread-create")
async def create_thread(payload: ThreadCreateRequest, db: AsyncSession = Depends(get_db)):
    """Create a new thread in PostgreSQL"""
    tid = str(uuid.uuid4())
    
    # Save thread to PostgreSQL
    thread = await DatabaseService.create_thread(db=db, user_id=payload.user_id, thread_id=tid)
    
    return {
        "thread_id": thread.thread_id,
        "user_id": thread.user_id,
        "created_at": thread.created_at.isoformat()
    }


@router.post("/user-threads")
async def get_user_threads(payload: UserThreadsRequest, db: AsyncSession = Depends(get_db)):
    """Get all threads for a user from PostgreSQL"""
    threads = await DatabaseService.get_user_threads(db, payload.user_id)
    
    return {
        "user_id": payload.user_id,
        "threads": [
            {
                "thread_id": t.thread_id,
                "created_at": t.created_at.isoformat(),
                "updated_at": t.updated_at.isoformat() if t.updated_at else None
            }
            for t in threads
        ]
    }


thread_endpoint = router