import reflex as rx
from sqlmodel import Field, func, Relationship
from datetime import datetime, timezone
from typing import List, Optional

class Conversations(rx.Model, table=True):
    """
    Modelo de conversaciones del chatbot con timestamps en UTC puro.
    Cada conversación está vinculada a un thread_id único de OpenAI.
    """
    
    # Clave primaria
    id: int | None = Field(default=None, primary_key=True)
    
    # Relación con mensajes (One-to-Many)
    messages: List["Messages"] = Relationship(back_populates="conversation")
    
    # Thread ID único de OpenAI (cada conversación tiene su propio thread)
    thread_id: str = Field(unique=True, index=True, max_length=255)
    
    # Título de la conversación (auto-generado desde el primer mensaje)
    title: str = Field(default="Nueva conversación", max_length=255, index=True)
    
    # Timestamps en UTC puro (conversión a timezone local en UI)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()},
        index=True
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
        index=True
    )
    
    def __repr__(self) -> str:
        """Representación en string del modelo."""
        return f"<Conversation(id={self.id}, title='{self.title}', thread_id='{self.thread_id}')>"
