from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.schemas.chat_schemas import ChatRequest, ChatResponse, ChatHistoryRequest
from app.services.chat_service import generate_chat_response_with_history
from app.services.database_service import DatabaseService
from app.database import get_db

# ---------- APP ----------
router = APIRouter()


# ---------- ROUTES ----------
@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Get or create thread
        thread = await DatabaseService.get_or_create_thread(
            db, 
            user_id=req.userID, 
            thread_id=req.threadID
        )
        
        # Save user message to PostgreSQL
        await DatabaseService.save_message(
            db,
            thread_id=thread.thread_id,
            user_id=req.userID,
            role="user",
            content=req.message
        )
        
        # Generate AI response with conversation history
        reply = await generate_chat_response_with_history(db, thread.thread_id, req.message)
        
        # Save assistant message to PostgreSQL
        await DatabaseService.save_message(
            db,
            thread_id=thread.thread_id,
            user_id=req.userID,
            role="assistant",
            content=reply
        )
        
        return ChatResponse(userId=req.userID, threadId=thread.thread_id, reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat-history")
async def get_chat_history(payload: ChatHistoryRequest, db: AsyncSession = Depends(get_db)):
    """Get all messages for a specific thread from PostgreSQL"""
    messages = await DatabaseService.get_thread_messages(db, payload.thread_id)
    
    return {
        "thread_id": payload.thread_id,
        "message_count": len(messages),
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }


chat_router = router