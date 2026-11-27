import os
from dotenv import load_dotenv
from openai import OpenAI

# read OPENAI_API_KEY from .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL") or None,
)
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
