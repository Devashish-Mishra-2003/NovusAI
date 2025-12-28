from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, HttpUrl
from typing import Optional


class Settings(BaseSettings):
    ENV: str = Field(default="development")

    # LLM
    OLLAMA_BASE_URL: HttpUrl = Field(default="http://localhost:11434")
    OLLAMA_MODEL: str = Field(default="phi3:mini")
    OLLAMA_TEMPERATURE: float = Field(default=0.2)

    # External APIs
    epo_ops_consumer_key: str
    epo_ops_consumer_secret: str

    # 🔐 JWT (ADD THESE)
    JWT_SECRET_KEY: str = Field(default="novusai-super-secret-key")
    JWT_ALGORITHM: str = Field(default="HS256")

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
