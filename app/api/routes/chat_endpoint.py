from fastapi import APIRouter, HTTPException
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import generate_chat_response

# ---------- APP ----------
router = APIRouter()


# ---------- ROUTES ----------
@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        reply = await generate_chat_response(req.message)
        return ChatResponse(userId=req.userID, threadId=req.threadID, reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


chat_router = router