from fastapi import FastAPI
from app.api.routes.chat_endpoint import chat_router
from app.api.routes.thread_endpoint import thread_endpoint


app = FastAPI(title="Async Chatbot API", version="1.0")

app.include_router(thread_endpoint)

app.include_router(chat_router)

