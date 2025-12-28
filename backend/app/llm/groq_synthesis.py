# app/llm/groq_synthesis.py

import logging
from openai import AsyncOpenAI

logger = logging.getLogger("groq-synthesis")

GROQ_API_KEY = "supersecretkey"  # ← Your key
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "llama-3.3-70b-versatile"  # Top-tier reasoning + speed

client = AsyncOpenAI(
    base_url=GROQ_BASE_URL,
    api_key=GROQ_API_KEY,
)

async def run_groq(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2048,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Groq synthesis failed: {e}")
        return "Sorry, I couldn't generate a response at this time."