import reflex as rx
from sqlmodel import Field, func, Relationship
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .conversations import Conversations

class Messages(rx.Model, table=True):
    """
    Modelo para almacenar los mensajes de cada conversación.
    Almacena el par pregunta-respuesta encriptados para privacidad.
    """
    
    id: int | None = Field(default=None, primary_key=True)
    
    # Vinculación con la conversación
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    conversation: Optional["Conversations"] = Relationship(back_populates="messages")
    
    # Contenido del mensaje (Debe almacenarse encriptado)
    question_encrypted: str = Field(default="")
    answer_encrypted: str = Field(default="")
    
    # Timestamp de creación
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()},
        index=True
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, conversation_id={self.conversation_id})>"
