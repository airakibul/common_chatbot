from pydantic import BaseModel

class ChatRequest(BaseModel):
    userID: str
    threadID: str
    message: str

class ChatResponse(BaseModel):
    userId: str
    threadId: str
    reply: str