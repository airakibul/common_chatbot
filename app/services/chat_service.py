from app.config import client
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.database_service import DatabaseService


async def get_conversation_history(db: AsyncSession, thread_id: str) -> str:
    """Fetch and format last 10 messages from database"""
    previous_messages = await DatabaseService.get_thread_messages(db, thread_id)
    last_10_messages = previous_messages[-10:] if len(previous_messages) > 10 else previous_messages
    
    conversation_history = ""
    if last_10_messages:
        conversation_history = "Conversation History:\n"
        for msg in last_10_messages:
            role_label = "User" if msg.role == "user" else "Assistant"
            conversation_history += f"{role_label}: {msg.content}\n"
            
    print(conversation_history)
    return conversation_history


async def generate_chat_response_with_history(db: AsyncSession, thread_id: str, message: str) -> str:
    """Generate chat response with conversation history from database"""
    conversation_history = await get_conversation_history(db, thread_id)
    return await generate_chat_response(message, conversation_history)


async def generate_chat_response(message: str, conversation_history: str = "") -> str:

    prompt = f"""

You are a helpful and concise AI assistant.

{conversation_history}

Current Message: "{message}"

---

Respond naturally and briefly, showing you understand their situation. If they need more detail, they'll ask:
"""


    try:
        completion = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        
        response_text = completion.choices[0].message.content.strip()
        print(f"DEBUG - LLM response:\n{response_text}")
        return response_text
    except Exception as e:
        print(f"ERROR in generate_chat_response - OpenAI API call failed: {str(e)}")
        raise