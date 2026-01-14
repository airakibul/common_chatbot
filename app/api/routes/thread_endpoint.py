from fastapi import APIRouter
import uuid
from pydantic import BaseModel

router = APIRouter()



class ThreadCreateRequest(BaseModel):
    user_id: str

@router.post("/chat-thread-create")
async def create_thread(payload: ThreadCreateRequest):
    tid = str(uuid.uuid4())
    return {"thread_id": tid}



thread_endpoint = router