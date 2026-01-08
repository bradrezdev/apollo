# state.py

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
    should_reopen_drawer: bool = False
    
    # === VARIABLES DE EDICIÓN DE CONVERSACIONES ===
    is_edit_dialog_open: bool = False
    conversation_to_edit_id: int | None = None
    new_conversation_title: str = ""
    
    # === VARIABLES DE ELIMINACIÓN DE CONVERSACIONES ===
    is_delete_dialog_open: bool = False
    conversation_to_delete_id: int | None = None
    
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
    
    @rx.var
    def current_conversation_title(self) -> str:
        """Obtiene el título de la conversación actual"""
        if not self.current_conversation_id:
            return ""
        
        for conv in self.conversations:
            if conv["id"] == self.current_conversation_id:
                return conv["title"]
        return ""
    
    # === MÉTODOS DE INICIALIZACIÓN ===
    def on_load(self):
        """Carga inicial de la aplicación"""
        print("[DEBUG] Ejecutando State.on_load", flush=True)
        return self.load_conversations()
        print("[DEBUG] Todo listo para usarse", flush=True)

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
        print(f"[DEBUG] Usuario envio mensaje: {message}")
        
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
                print("[DEBUG] No hay thread_id activo. Creando nuevo thread en OpenAI...")
                thread = await client.beta.threads.create()
                print(f"[DEBUG] Thread creado en OpenAI: {thread.id}")
                
                new_id = self.create_new_conversation(
                    thread_id=thread.id,
                    title="Nueva conversación"
                )
                
                if not new_id:
                    raise Exception("Fallo al guardar la conversación en base de datos")
                    
                print(f"[DEBUG] Conversación guardada en BD. ID: {new_id}, Thread: {self.current_thread_id}")
            
            print(f"[DEBUG] Enviando mensaje al thread: {self.current_thread_id}")
            
            # Enviar mensaje del usuario al thread actual
            await client.beta.threads.messages.create(
                thread_id=self.current_thread_id,
                role="user",
                content=message
            )
            
            # Inicializar variable para respuesta en streaming
            answer = ""
            yield
            
            # Usar create_and_stream() para streaming en tiempo real
            async with client.beta.threads.runs.create_and_stream(
                thread_id=self.current_thread_id,
                assistant_id=API_ASSISTANT_ID,
            ) as stream:
                # Iterar sobre text_deltas - streaming palabra por palabra
                async for text_delta in stream.text_deltas:
                    answer += text_delta
                    # Reasignar la lista completa para que Reflex detecte el cambio
                    updated_history = self.chat_history.copy()
                    updated_history[-1] = (updated_history[-1][0], answer)
                    self.chat_history = updated_history
                    yield
                
            # Actualizar timestamp de la conversación
            if self.current_conversation_id:
                self.update_conversation_timestamp(self.current_conversation_id)
            
            # Auto-generar título si es el primer mensaje
            if len(self.chat_history) == 1 and self.current_conversation_id:
                await self.auto_generate_title(answer)
            
            # Recargar conversaciones para actualizar el orden
            self.load_conversations()
            
            print(f"[DEBUG] Chatbot respondio: {answer}")
                            
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
        if self.is_open:
            print("[DEBUG] Drawer abierto")
        else:
            print("[DEBUG] Drawer cerrado")
    
    @rx.event
    def open_drawer(self):
        """Abre el drawer"""
        self.is_open = True
        print("[DEBUG] Drawer abierto")
    
    @rx.event
    def close_drawer(self):
        """Cierra el drawer"""
        self.is_open = False
        print("[DEBUG] Drawer cerrado")
    
    @rx.event
    def log_copy_event(self):
        """Registra evento de copiado"""
        print("[DEBUG] Respuesta copiada exitosamente")
    
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
    
    @rx.event
    def log_context_menu_open(self, is_open: bool):
        """Registra cuando se abre el menú contextual"""
        if is_open:
            print("[DEBUG] Context menu abierto")

    # === MÉTODOS DE GESTIÓN DE CONVERSACIONES (CRUD) ===
    @rx.event
    def reopen_drawer_if_needed(self):
        """Reabre el drawer solo si la bandera should_reopen_drawer es True"""
        if self.should_reopen_drawer:
            self.is_open = True
            self.should_reopen_drawer = False

    @rx.event
    def open_edit_dialog(self, conversation_id: int, current_title: str):
        """
        Abre el diálogo de edición de título
        
        Args:
            conversation_id: ID de la conversación a editar
            current_title: Título actual de la conversación
        """
        print("[DEBUG] Opcion seleccionada: Editar título")
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
            new_title = self.new_conversation_title.strip()
            self.update_conversation_title(
                self.conversation_to_edit_id,
                new_title
            )
            print(f"[DEBUG] Titulo actualizado exitosamente a: {new_title}")
            self.close_edit_dialog()
    
    @rx.event
    def open_delete_dialog(self, conversation_id: int):
        """
        Abre el diálogo de confirmación de eliminación
        
        Args:
            conversation_id: ID de la conversación a eliminar
        """
        print("[DEBUG] Opcion seleccionada: Eliminar conversación")
        self.conversation_to_delete_id = conversation_id
        self.is_delete_dialog_open = True

    @rx.event
    def close_delete_dialog(self):
        """Cierra el diálogo de eliminación"""
        self.is_delete_dialog_open = False
        self.conversation_to_delete_id = None

    @rx.event
    def confirm_delete_conversation(self):
        """Confirma la eliminación de la conversación"""
        if self.conversation_to_delete_id:
            self.delete_conversation(self.conversation_to_delete_id)
            # Si eliminamos la conversación actual, limpiar el chat
            if self.current_conversation_id == self.conversation_to_delete_id:
                self.chat_history = []
            self.close_delete_dialog()
    
    # === MÉTODOS DE GESTIÓN DE CONVERSACIONES ===
    async def auto_generate_title(self, answer_text: str):
        """
        Genera automáticamente un título basado en la respuesta del asistente
        
        Args:
            answer_text: Respuesta del asistente
        """
        if not self.current_conversation_id:
            return
            
        try:
            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            
            # Generar título usando GPT
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto creando títulos cortos y concisos para conversaciones."},
                    {"role": "user", "content": f"Crea el título de la conversación con base a un resumen sobre la respuesta que el asistente dio. La respuesta es: {answer_text}"}
                ],
                max_tokens=15,
                temperature=0.5,
            )
            
            title = response.choices[0].message.content.strip().replace('"', '')
            
            # Asegurar que no sea muy largo
            if len(title) > 40:
                title = title[:37] + "..."
                
            self.update_conversation_title(self.current_conversation_id, title)
            
        except Exception as e:
            print(f"Error generando título con IA: {e}")
            # Fallback: Usar primeros caracteres
            title = answer_text[:30] + "..." if len(answer_text) > 30 else answer_text
            self.update_conversation_title(self.current_conversation_id, title)
    
    def start_new_conversation(self):
        """Inicia una nueva conversación limpiando el estado actual"""
        self.current_conversation_id = None
        self.current_thread_id = ""
        self.chat_history = []
        print("[DEBUG] Nueva conversacion iniciada")
    
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
            
            print(f"[DEBUG] Cambio de conversacion a: {conversation['title']}")
            
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