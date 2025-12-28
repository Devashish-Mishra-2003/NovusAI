# app/models/chat.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON  # works with SQLite & Postgres

from app.db import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    # === NEW: PERSISTED CONTEXT (MINIMAL) ===
    conditions = Column(JSON, nullable=True)        # ["nash"]
    active_drugs = Column(JSON, nullable=True)      # ["metformin", "semaglutide"]
    intent = Column(String, nullable=True)           # CLINICAL / COMMERCIAL / FULL_OPPORTUNITY
    mode = Column(String, nullable=True)             # SINGLE / COMPARISON

    visualizations_json = Column(Text, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")