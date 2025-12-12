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
    
    # === VARIABLES DE EDICIÓN DE CONVERSACIONES ===
    is_edit_dialog_open: bool = False
    conversation_to_edit_id: int | None = None
    new_conversation_title: str = ""
    
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
    async def answer(self, form_data: dict = None):
        """
        Procesa la pregunta del usuario y obtiene respuesta del assistant mediante streaming
        
        Args:
            form_data: Diccionario con los datos del formulario (requerido por rx.form)
        
        Implementación basada en OpenAI Assistants API v2 (beta)
        Documentación: https://platform.openai.com/docs/api-reference/assistants
        """
        # Usar form_data si está disponible, sino usar self.question
        if form_data and "question" in form_data:
            question_text = form_data["question"]
        else:
            question_text = self.question
        
        if not question_text or not question_text.strip():
            return
        
        message = question_text.strip()
        print(f"🚀 Iniciando respuesta para: '{message}'")
        
        # Agregar mensaje del usuario inmediatamente al historial
        self.chat_history = self.chat_history + [(message, "")]
        self.question = ""
        
        # Activar estado de carga (el asistente está "pensando")
        self.is_loading = True
        yield
        
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
            
            # Inicializar variable para respuesta en streaming
            answer = ""
            print(f"📋 Mensaje agregado al historial. Total: {len(self.chat_history)}")
            yield
            
            # Usar create_and_stream() para streaming en tiempo real
            print(f"🤖 Iniciando streaming con assistant {API_ASSISTANT_ID}...")
            async with client.beta.threads.runs.create_and_stream(
                thread_id=self.current_thread_id,
                assistant_id=API_ASSISTANT_ID,
            ) as stream:
                # Iterar sobre text_deltas - streaming palabra por palabra
                print("📥 Procesando text deltas en streaming...")
                async for text_delta in stream.text_deltas:
                    answer += text_delta
                    # Reasignar la lista completa para que Reflex detecte el cambio
                    updated_history = self.chat_history.copy()
                    updated_history[-1] = (updated_history[-1][0], answer)
                    self.chat_history = updated_history
                    print(f"📝 Streaming: '{text_delta}' | Total: {len(answer)} caracteres")
                    yield
                
                print("✅ Streaming completado exitosamente")
            
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
    
    # === MÉTODOS DE GESTIÓN DE CONVERSACIONES (CRUD) ===
    @rx.event
    def open_edit_dialog(self, conversation_id: int, current_title: str):
        """
        Abre el diálogo de edición de título
        
        Args:
            conversation_id: ID de la conversación a editar
            current_title: Título actual de la conversación
        """
        self.conversation_to_edit_id = conversation_id
        self.new_conversation_title = current_title
        self.is_edit_dialog_open = True
    
    @rx.event
    def close_edit_dialog(self):
        """Cierra el diálogo de edición"""
        self.is_edit_dialog_open = False
        self.conversation_to_edit_id = None
        self.new_conversation_title = ""
    
    @rx.event
    def save_conversation_title(self):
        """Guarda el nuevo título de la conversación"""
        if self.conversation_to_edit_id and self.new_conversation_title.strip():
            self.update_conversation_title(
                self.conversation_to_edit_id,
                self.new_conversation_title.strip()
            )
            self.close_edit_dialog()
    
    @rx.event
    def delete_conversation_confirm(self, conversation_id: int):
        """
        Elimina una conversación
        
        Args:
            conversation_id: ID de la conversación a eliminar
        """
        self.delete_conversation(conversation_id)
        # Si eliminamos la conversación actual, limpiar el chat
        if self.current_conversation_id == conversation_id:
            self.chat_history = []
    
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