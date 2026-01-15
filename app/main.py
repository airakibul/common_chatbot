from fastapi import FastAPI
from app.api.routes.chat_endpoint import chat_router
from app.api.routes.thread_endpoint import thread_endpoint
from app.database import init_db


app = FastAPI(title="Async Chatbot API", version="1.0")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()


app.include_router(thread_endpoint, tags=["threads"])

app.include_router(chat_router, tags=["chat"])
