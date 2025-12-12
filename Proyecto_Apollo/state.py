# state.py

import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import reflex as rx
from Proyecto_Apollo.config import OPENAI_API_KEY, API_ASSISTANT_ID
from db.db_state import DBState

# Cargar variables de entorno
load_dotenv()


class State(DBState):
    """Estado principal que maneja la funcionalidad del chat (hereda DBState para operaciones de BD)"""
    
    # === VARIABLES DEL CHAT ===
    question: str = ""
    chat_history: list[tuple[str, str]] = []
    is_loading: bool = False
    
    # === VARIABLES DEL DRAWER ===
    is_open: bool = False
    
    # === VARIABLES DE UI ===
    auto_scroll_enabled: bool = True
    user_name: str = "Bryan Nuñez"
    user_email: str = "b.nunez@hotmail.es"
    
    # === COMPUTED VARS ===
    @rx.var
    def has_messages(self) -> bool:
        """Indica si hay mensajes en el historial"""
        return len(self.chat_history) > 0
    
    @rx.var
    def message_count(self) -> int:
        """Número de mensajes en el historial"""
        return len(self.chat_history)
    
    # === MÉTODOS DEL CHAT ===
    async def answer(self):
        """
        Procesa la pregunta del usuario y obtiene respuesta del assistant mediante streaming
        
        Implementación basada en OpenAI Assistants API v2 (beta)
        Documentación: https://platform.openai.com/docs/api-reference/assistants
        """
        if not self.question.strip():
            return
        
        # Activar estado de carga
        self.is_loading = True
        yield
            
        message = self.question.strip()
        print(f"🚀 Iniciando respuesta para: '{message}'")
        
        try:
            # Inicializar cliente OpenAI
            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            
            # Si no hay conversación activa, crear una nueva
            if not self.current_thread_id:
                print("🆕 Creando nuevo thread...")
                thread = await client.beta.threads.create()
                self.create_new_conversation(
                    thread_id=thread.id,
                    title="Nueva conversación"
                )
                print(f"✅ Thread creado: {thread.id}")
            
            # Enviar mensaje del usuario al thread actual
            print(f"📤 Enviando mensaje al thread {self.current_thread_id}...")
            await client.beta.threads.messages.create(
                thread_id=self.current_thread_id,
                role="user",
                content=message
            )
            
            # Limpiar la pregunta del input
            self.question = ""
            yield
            
            # Crear el run y esperar a que se complete (sin streaming)
            print(f"🤖 Iniciando run con assistant {API_ASSISTANT_ID}...")
            run = await client.beta.threads.runs.create_and_poll(
                thread_id=self.current_thread_id,
                assistant_id=API_ASSISTANT_ID,
            )
            print(f"✅ Run completado con estado: {run.status}")
            
            # Obtener todos los mensajes del thread
            messages = await client.beta.threads.messages.list(
                thread_id=self.current_thread_id,
                order="desc",
                limit=1
            )
            
            # Extraer la respuesta del asistente
            answer = ""
            if messages.data and len(messages.data) > 0:
                last_message = messages.data[0]
                if last_message.role == "assistant" and last_message.content:
                    first_content = last_message.content[0]
                    if first_content.type == "text":
                        answer = first_content.text.value  # type: ignore
            
            print(f"📝 Respuesta recibida: {len(answer)} caracteres")
            
            # Agregar al historial una vez que tengamos la respuesta completa
            self.chat_history = self.chat_history + [(message, answer)]
            yield
            
            # Actualizar timestamp de la conversación
            if self.current_conversation_id:
                self.update_conversation_timestamp(self.current_conversation_id)
            
            # Auto-generar título si es el primer mensaje
            if len(self.chat_history) == 1 and self.current_conversation_id:
                self.auto_generate_title(message)
            
            # Recargar conversaciones para actualizar el orden
            self.load_conversations()
            
            print("🎉 Respuesta completada")
                            
        except Exception as e:
            # Manejo de errores detallado
            error_message = f"Error al procesar la solicitud: {str(e)}"
            print(f"❌ Error: {error_message}")
            
            # Mostrar error en el chat
            if self.chat_history and self.chat_history[-1][0] == message:
                updated_history = self.chat_history.copy()
                updated_history[-1] = (message, f"⚠️ {error_message}")
                self.chat_history = updated_history
            else:
                self.chat_history = self.chat_history + [(message, f"⚠️ {error_message}")]
            
            self.question = ""
            yield
        
        finally:
            # Desactivar estado de carga
            self.is_loading = False
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
    
    # === MÉTODOS DE GESTIÓN DE CONVERSACIONES ===
    def auto_generate_title(self, first_message: str):
        """
        Genera automáticamente un título basado en el primer mensaje
        
        Args:
            first_message: Primer mensaje del usuario
        """
        if not self.current_conversation_id:
            return
        
        # Usar el primer mensaje como título (máximo 50 caracteres)
        title = first_message[:50] + "..." if len(first_message) > 50 else first_message
        self.update_conversation_title(self.current_conversation_id, title)
    
    def start_new_conversation(self):
        """Inicia una nueva conversación limpiando el estado actual"""
        self.current_conversation_id = None
        self.current_thread_id = ""
        self.chat_history = []
    
    async def load_conversation_and_messages(self, conversation_id: int):
        """
        Carga una conversación y sus mensajes desde OpenAI
        
        Args:
            conversation_id: ID de la conversación a cargar
        """
        try:
            # Cargar datos de la conversación desde la BD
            conversation = self.load_conversation_by_id(conversation_id)
            
            if not conversation:
                return
            
            # Obtener mensajes del thread desde OpenAI
            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            messages = await client.beta.threads.messages.list(
                thread_id=conversation["thread_id"],
                order="asc"
            )
            
            # Convertir a formato de chat_history
            new_history = []
            temp_question = ""
            
            for msg in messages.data:
                # Extraer contenido de texto solo si existe
                content = ""
                if msg.content and len(msg.content) > 0:
                    first_content = msg.content[0]
                    # Type guard: verificar que sea TextContentBlock
                    if first_content.type == "text":
                        content = first_content.text.value  # type: ignore
                
                if msg.role == "user":
                    temp_question = content
                elif msg.role == "assistant" and temp_question:
                    new_history.append((temp_question, content))
                    temp_question = ""
            
            self.chat_history = new_history
            yield
            
        except Exception as e:
            print(f"Error cargando mensajes de la conversación: {e}")