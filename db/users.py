import reflex as rx
from sqlmodel import Field, Relationship
from typing import List, Optional

class Users(rx.Model, table=True):
    """
    Modelo de usuarios del sistema con autenticación.
    """
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    fecha_de_nacimiento: str = Field(max_length=50)
    correo: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    salt: str = Field(max_length=255, default="")
    
    # Supabase auth ID (opcional si usan Supabase Auth puro)
    supabase_uid: Optional[str] = Field(default=None, index=True, max_length=255)
    
    bo_connection: bool = Field(default=False)
    
    # Relación One-to-Many con Conversations
    conversations: List["Conversations"] = Relationship(back_populates="user")
