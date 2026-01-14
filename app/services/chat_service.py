from app.config import client

async def generate_chat_response(message: str) -> str:

    prompt = f"""

You are a helpful and concise AI assistant.



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