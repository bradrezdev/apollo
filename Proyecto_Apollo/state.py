# state.py

import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import reflex as rx
from Proyecto_Apollo.api_keys import OPENAI_API_KEY, API_ASSISTANT_ID

# Cargar variables de entorno
load_dotenv()


class State(rx.State):
    """Estado principal que maneja toda la funcionalidad del proyecto"""
    
    # === VARIABLES DEL CHAT ===
    question: str = ""
    chat_history: list[tuple[str, str]] = []
    
    # === VARIABLES DEL DRAWER ===
    is_open: bool = False
    
    # === VARIABLES DE UI ===
    auto_scroll_enabled: bool = True
    user_name: str = "Bryan Nuñez"
    user_email: str = "b.nunez@hotmail.es"
    
    # === MÉTODOS DEL CHAT ===
    async def answer(self):
        """Procesa la pregunta del usuario y obtiene respuesta del assistant"""
        if not self.question.strip():
            return
            
        message = self.question.strip()
        
        try:
            # Inicializar cliente OpenAI
            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            
            # Crear thread
            thread = await client.beta.threads.create()
            
            # Enviar mensaje del usuario
            await client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=message
            )
            
            # Iniciar streaming del assistant
            session = await client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=API_ASSISTANT_ID,
                stream=True,
            )
            
            # Inicializar respuesta y actualizar UI
            answer = ""
            self.chat_history.append((message, answer))
            self.question = ""
            yield
            
            # Procesar respuesta en streaming
            async for event in session:
                if (event.event == "thread.message.delta" 
                    and event.data.delta.content):
                    
                    for content_block in event.data.delta.content:
                        if (content_block.type == "text" 
                            and content_block.text 
                            and content_block.text.value):
                            
                            answer += content_block.text.value
                            self.chat_history[-1] = (
                                self.chat_history[-1][0],
                                answer,
                            )
                            yield
                            
        except Exception as e:
            # Manejo de errores
            error_message = f"Error al procesar la solicitud: {str(e)}"
            self.chat_history.append((message, error_message))
            self.question = ""
            yield
    
    # === MÉTODOS DEL DRAWER ===
    @rx.event
    def toggle_drawer(self):
        """Alterna el estado del drawer"""
        self.is_open = not self.is_open
    
    @rx.event
    def open_drawer(self):
        """Abre el drawer"""
        self.is_open = True
    
    @rx.event
    def close_drawer(self):
        """Cierra el drawer"""
        self.is_open = False
    
    # === MÉTODOS DE UI ===
    @rx.event
    def toggle_auto_scroll(self):
        """Alterna el scroll automático"""
        self.auto_scroll_enabled = not self.auto_scroll_enabled
    
    @rx.event
    def clear_chat_history(self):
        """Limpia el historial del chat"""
        self.chat_history = []
    
    @rx.event
    def update_user_info(self, name: str, email: str):
        """Actualiza la información del usuario"""
        self.user_name = name
        self.user_email = email