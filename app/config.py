import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# ---------- CONFIG ----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

# PostgreSQL Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)