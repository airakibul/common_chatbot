from pydantic import BaseModel



class ChatRequest(BaseModel):
    userID: str
    threadID: str
    message: str



class ChatResponse(BaseModel):
    userId: str
    threadId: str
    reply: str
    
    
    
class ChatHistoryRequest(BaseModel):
    thread_id: str
    
    
    
class ThreadCreateRequest(BaseModel):
    user_id: str




class UserThreadsRequest(BaseModel):
    user_id: str
