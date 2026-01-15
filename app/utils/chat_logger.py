import json
import os
from datetime import datetime
from typing import List, Dict

CHAT_LOG_FILE = "chat_history.json"


def load_chat_history() -> List[Dict]:
    """Load chat history from file"""
    if not os.path.exists(CHAT_LOG_FILE):
        return []
    
    try:
        with open(CHAT_LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def save_chat_message(user_id: str, thread_id: str, role: str, message: str) -> Dict:
    """Save a chat message to file"""
    history = load_chat_history()
    
    chat_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "thread_id": thread_id,
        "role": role,
        "message": message
    }
    
    history.append(chat_entry)
    
    # Save to file
    with open(CHAT_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    
    print(f"✅ SAVED: {role} message for user {user_id} in thread {thread_id}")
    return chat_entry


def get_thread_messages(thread_id: str) -> List[Dict]:
    """Get all messages for a specific thread"""
    history = load_chat_history()
    return [msg for msg in history if msg.get("thread_id") == thread_id]


def get_user_threads(user_id: str) -> List[str]:
    """Get all thread IDs for a user"""
    history = load_chat_history()
    threads = set()
    for msg in history:
        if msg.get("user_id") == user_id:
            threads.add(msg.get("thread_id"))
    return list(threads)
