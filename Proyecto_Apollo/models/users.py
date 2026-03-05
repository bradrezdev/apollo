import reflex as rx
from sqlmodel import Field, Relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .conversations import Conversations

class Users(rx.Model, table=True):
    """
    Modelo de usuarios local del sistema Apollo.
    """
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    fecha_de_nacimiento: str = Field(max_length=50)
    correo: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    salt: str = Field(max_length=255, default="")
    
    supabase_uid: Optional[str] = Field(default=None, index=True, max_length=255)
    
    bo_connection: bool = Field(default=False)
    
    conversations: List["Conversations"] = Relationship(back_populates="user")
