from typing import TypedDict, Annotated
import operator
from langgraph.graph import MessagesState
from langchain_ollama import ChatOllama

from app.config import settings

State = MessagesState

llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=str(settings.OLLAMA_BASE_URL),
    temperature=settings.OLLAMA_TEMPERATURE
)
