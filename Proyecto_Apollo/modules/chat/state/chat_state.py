from openai import AsyncOpenAI
from dotenv import load_dotenv
import reflex as rx
from Proyecto_Apollo.config import OPENAI_API_KEY, API_ASSISTANT_ID
from .db_state import DBState
import asyncio
import re
from datetime import datetime

# Cargar variables de entorno
load_dotenv()


class State(DBState):
    """Estado principal optimizado que maneja la funcionalidad del chat con UI no bloqueante"""
    
    # === SANITIZACIÓN DE RESPUESTAS OpenAI ===
    @staticmethod
    def _sanitize_response(text: str) -> str:
        """
        Elimina artefactos de citación del OpenAI Assistants API.
        
        Patrones eliminados:
        - fileciteturnXfileY (ej: fileciteturn7file4)
        - 【...】 (corchetes CJK con contenido de citación)
        - 【†source】 y variantes
        - sandbox:/mnt/... rutas internas
        """
        if not text:
            return text
        
        # Patrón 1: fileciteturnXfileY (con o sin espacios alrededor)
        text = re.sub(r'\s*filecite\w*', '', text)
        
        # Patrón 2: Corchetes CJK con contenido de citación 【...】
        text = re.sub(r'【[^】]*】', '', text)
        
        # Patrón 3: Rutas sandbox internas
        text = re.sub(r'sandbox:/mnt/\S+', '', text)
        
        # Patrón 4: Anotaciones residuales tipo [数字:数字†source]
        text = re.sub(r'\[\d+:\d+†[^\]]*\]', '', text)
        
        # Limpiar espacios dobles residuales
        text = re.sub(r'  +', ' ', text)
        
        return text.strip()
    
    # === VARIABLES DEL CHAT ===
    question: str = ""
    chat_history: list[tuple[str, str]] = []
    is_loading: bool = False
    
    # === VARIABLES DEL DRAWER OPTIMIZADAS ===
    is_open: bool = False
    should_reopen_drawer: bool = False
    drawer_loading: bool = False  # Solo para UI del drawer
    drawer_loaded_once: bool = False  # Para saber si ya cargamos conversaciones
    
    # === VARIABLES DE EDICIÓN DE CONVERSACIONES ===
    is_edit_dialog_open: bool = False
    conversation_to_edit_id: int | None = None
    new_conversation_title: str = ""
    
    # === VARIABLES DE ELIMINACIÓN DE CONVERSACIONES ===
    is_delete_dialog_open: bool = False
    conversation_to_delete_id: int | None = None
    
    # === VARIABLES DE UI OPTIMIZADAS ===
    auto_scroll_enabled: bool = True
    is_profile_drawer_open: bool = False
    
    @rx.var
    def user_name(self) -> str:
        """Nombre del usuario autenticado.

        Orden de prioridad:
        1. display_name cargado desde la BD local (nombre + apellido real del usuario)
        2. user_metadata del JWT de Supabase (solo si el nombre aún no fue guardado en BD)
        3. Fallback: "Usuario"
        """
        if self.display_name:
            return self.display_name
        if self.user_metadata:
            first = self.user_metadata.get("first_name", "")
            last = self.user_metadata.get("last_name", "")
            if first or last:
                return f"{first} {last}".strip()
        return "Usuario"

    @rx.var
    def user_email(self) -> str:
        """Email del usuario autenticado.

        Lee desde display_email (cargado desde Users.correo en la BD local).
        Suplex.user_email depende de JWT decode con JWKS (ES256) lo cual puede
        fallar o estar pendiente en dev. Este override garantiza que el email
        siempre se muestre si el usuario está en la BD local.
        """
        return self.display_email
    
    # === VARIABLES PARA SCROLL INFINITO ===
    visible_conversations_start: int = 0
    visible_conversations_end: int = 20
    
    # === COMPUTED VARS OPTIMIZADAS ===
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
        """Obtiene el título de la conversación actual desde cache"""
        if not self.current_conversation_id:
            return ""
        
        conv = self.get_current_conversation()
        return conv["title"] if conv else ""
    
    @rx.var
    def visible_conversations(self) -> list[dict]:
        """Conversaciones visibles para scroll infinito (carga progresiva)"""
        if not self.conversations:
            return []
        
        # Mostrar solo las conversaciones en el viewport virtual
        end_idx = min(self.visible_conversations_end, len(self.conversations))
        return self.conversations[self.visible_conversations_start:end_idx]
    
    @rx.var
    def has_more_conversations(self) -> bool:
        """Indica si hay más conversaciones por cargar"""
        return self.visible_conversations_end < len(self.conversations)
    
    # === MÉTODOS DE INICIALIZACIÓN OPTIMIZADOS ===
    async def on_load(self):
        """Carga inicial ASÍNCRONA de la aplicación"""
        print("[DEBUG] Ejecutando State.on_load optimizado", flush=True)
        
        # ── Auth guard con soporte de refresh ──────────────────────
        # 1. Si hay access_token, la sesión está activa → continuar
        # 2. Si no hay access_token pero sí refresh_token → intentar renovar
        # 3. Sin ningún token → redirigir a login
        if not self.access_token:
            if self.refresh_token:
                print("[DEBUG] No hay access_token, intentando refresh con refresh_token...", flush=True)
                try:
                    self.refresh_session()
                    if self.access_token:
                        print("[DEBUG] Sesión renovada exitosamente via refresh_token", flush=True)
                    else:
                        print("[DEBUG] refresh_session no restauró el access_token", flush=True)
                        return rx.redirect("/")
                except Exception as e:
                    print(f"[DEBUG] refresh_session falló: {e}", flush=True)
                    return rx.redirect("/")
            else:
                print("[DEBUG] No hay access_token ni refresh_token, redirigiendo a inicio.", flush=True)
                return rx.redirect("/")
        
        # Iniciar carga de conversaciones en background SIN BLOQUEAR
        # Retornamos el generador asíncrono para que Reflex lo ejecute
        # El primer yield ocurre inmediatamente, permitiendo que la UI renderice
        return self.load_conversations_async()
    
    # === MÉTODOS DEL CHAT OPTIMIZADOS ===
    async def answer(self, form_data: dict = None):
        """
        Procesa la pregunta del usuario de forma optimizada
        """
        # Usar form_data si está disponible, sino usar self.question
        if form_data and "question" in form_data:
            question_text = form_data["question"]
        else:
            question_text = self.question
        
        if not question_text or not question_text.strip():
            return
        
        message = question_text.strip()
        print(f"[DEBUG] 💬 Usuario envió mensaje: {message[:50]}...")
        
        # Agregar mensaje del usuario inmediatamente al historial
        self.chat_history = self.chat_history + [(message, "")]
        self.question = ""
        
        # Activar estado de carga (el asistente está "pensando")
        self.is_loading = True
        yield  # ⭐ Mostrar spinner inmediatamente
        
        try:
            # Inicializar cliente OpenAI
            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            
            # Si no hay conversación activa, crear una nueva
            if not self.current_thread_id:
                print("[DEBUG] 🆕 No hay thread_id activo. Creando nuevo thread en OpenAI...")
                thread = await client.beta.threads.create()
                print(f"[DEBUG] ✅ Thread creado en OpenAI: {thread.id}")
                
                # ⭐ USAR VERSIÓN ASÍNCRONA OPTIMIZADA
                new_id = await self.create_new_conversation_async(
                    thread_id=thread.id,
                    title="Nueva conversación"
                )
                
                if not new_id:
                    raise Exception("Fallo al guardar la conversación en base de datos")
                    
                print(f"[DEBUG] ✅ Conversación guardada en BD. ID: {new_id}")
            
            print(f"[DEBUG] 📤 Enviando mensaje al thread: {self.current_thread_id}")
            
            # Enviar mensaje del usuario al thread actual
            await client.beta.threads.messages.create(
                thread_id=self.current_thread_id,
                role="user",
                content=message
            )
            
            yield
            
            # Usar create_and_stream() para streaming en tiempo real
            # Guardamos respuesta cruda para sanitizar sobre el acumulado completo
            raw_answer = ""
            async with client.beta.threads.runs.create_and_stream(
                thread_id=self.current_thread_id,
                assistant_id=API_ASSISTANT_ID,
            ) as stream:
                # Iterar sobre text_deltas - streaming palabra por palabra
                async for text_delta in stream.text_deltas:
                    raw_answer += text_delta
                    # Sanitizar el acumulado completo (tokens de citación pueden llegar partidos entre deltas)
                    answer = self._sanitize_response(raw_answer)
                    # Reasignar la lista completa para que Reflex detecte el cambio
                    updated_history = self.chat_history.copy()
                    updated_history[-1] = (updated_history[-1][0], answer)
                    self.chat_history = updated_history
                    yield  # ⭐ Actualizar UI con cada palabra
                
            # Sanitización final sobre la respuesta completa
            answer = self._sanitize_response(raw_answer)
            
            # ⭐ GUARDAR MENSAJE SANITIZADO EN SUPABASE ASÍNCRONAMENTE
            if self.current_conversation_id:
                print(f"[DEBUG] 💾 Guardando mensaje en BD: {message[:20]}...")
                asyncio.create_task(self.add_message_async(
                    self.current_conversation_id,
                    message,
                    answer
                ))

            # ⭐ ACTUALIZAR TIMESTAMP DE FORMA ASÍNCRONA (NO BLOQUEANTE)
            if self.current_conversation_id:
                asyncio.create_task(self.update_conversation_timestamp_async(self.current_conversation_id))
            
            # Auto-generar título si es el primer mensaje (en background)
            if len(self.chat_history) == 1 and self.current_conversation_id:
                asyncio.create_task(self.auto_generate_title_async(answer))
            
            # ⭐ RECARGAR CONVERSACIONES EN BACKGROUND (no bloquea)
            # Como load_conversations_async es un generador, debemos iterarlo si queremos que se ejecute en el event loop principal
            # o llamar a una función auxiliar wrapper.
            # En este caso, simplemente marcamos para recargar en la próxima oportunidad o usamos una tarea que itere
            asyncio.create_task(self._reload_conversations_wrapper())
            
            print(f"[DEBUG] 🤖 Chatbot respondió: {answer[:100]}...")
                            
        except Exception as e:
            # Manejo de errores detallado
            error_message = f"Error al procesar la solicitud: {str(e)}"
            print(f"❌ [ERROR] {error_message}")
            
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
    
    # === MÉTODOS DEL DRAWER OPTIMIZADOS ===
    async def _reload_conversations_wrapper(self):
        """Wrapper para recargar conversaciones en background (itera el generador)"""
        async for _ in self.load_conversations_async():
            pass

    async def toggle_drawer_optimized(self):
        """Alterna el estado del drawer con carga inteligente"""
        if self.is_open:
            # Si está abierto, simplemente cerrar
            self.is_open = False
            print("[DEBUG] 🪟 Drawer cerrado")
        else:
            # Si está cerrado, abrir y cargar si es necesario
            self.is_open = True
            print("[DEBUG] 🪟 Drawer abriendo...")
            
            # Solo cargar conversaciones si no se han cargado antes
            if not self.drawer_loaded_once and not self.is_loading_conversations:
                self.drawer_loading = True
                yield  # ⭐ Mostrar spinner en drawer inmediatamente
                
                # Cargar conversaciones de forma asíncrona (iterar generador)
                async for _ in self.load_conversations_async():
                    pass
                self.drawer_loaded_once = True
            
            self.drawer_loading = False
    
    @rx.event
    def toggle_drawer(self):
        """Wrapper para el evento toggle_drawer"""
        return self.toggle_drawer_optimized()
    
    @rx.event
    def open_drawer(self):
        """Abre el drawer con carga inteligente"""
        # Si ya está abierto, no hacer nada
        if self.is_open:
            return
        
        self.is_open = True
        print("[DEBUG] 🪟 Drawer abierto a petición")
        
        # Cargar conversaciones si es la primera vez
        if not self.drawer_loaded_once:
            return self._load_conversations_for_drawer()
    
    async def _load_conversations_for_drawer(self):
        """Carga conversaciones para el drawer sin bloquear"""
        self.drawer_loading = True
        yield
        
        async for _ in self.load_conversations_async():
             pass
        self.drawer_loaded_once = True
        
        self.drawer_loading = False
        yield
    
    @rx.event
    def close_drawer(self):
        """Cierra el drawer"""
        self.is_open = False
        print("[DEBUG] 🪟 Drawer cerrado")
    
    @rx.event
    def log_copy_event(self):
        """Registra evento de copiado"""
        print("[DEBUG] 📋 Respuesta copiada exitosamente")
    
    # === MÉTODOS DE SCROLL INFINITO PARA DRAWER ===
    def on_drawer_scroll(self, scroll_info: dict):
        """
        Maneja el scroll en el drawer para carga progresiva
        scroll_info: {"scrollTop": 100, "scrollHeight": 500, "clientHeight": 200}
        """
        if not scroll_info or "scrollTop" not in scroll_info:
            return
        
        # Calcular si estamos cerca del final (último 20%)
        scroll_top = scroll_info.get("scrollTop", 0)
        scroll_height = scroll_info.get("scrollHeight", 0)
        client_height = scroll_info.get("clientHeight", 0)
        
        if scroll_height <= 0 or client_height <= 0:
            return
        
        # Estamos en el 80% del scroll
        scroll_percentage = (scroll_top + client_height) / scroll_height
        
        if scroll_percentage > 0.8 and self.has_more_conversations:
            # Cargar más conversaciones
            self.visible_conversations_end += 10
            print(f"[DEBUG] 🔄 Cargando más conversaciones... ({self.visible_conversations_end}/{len(self.conversations)})")
    
    @rx.event
    def load_more_conversations(self):
        """Carga más conversaciones para scroll infinito"""
        if self.has_more_conversations:
            self.visible_conversations_end = min(
                self.visible_conversations_end + 20,
                len(self.conversations)
            )
            print(f"[DEBUG] 📚 Mostrando {self.visible_conversations_end} de {len(self.conversations)} conversaciones")
    
    @rx.event
    def reset_scroll_position(self):
        """Resetea la posición del scroll al cambiar de vista"""
        self.visible_conversations_start = 0
        self.visible_conversations_end = 20
    
    # === MÉTODOS DE UI ===
    @rx.event
    def toggle_profile_drawer(self):
        """Alterna el drawer de perfil (usado en on_click — sin argumentos).

        Al abrir el profile drawer desde dentro del mobile sidebar drawer,
        cierra el sidebar (is_open=False) para evitar que ambos drawers queden
        apilados visualmente y el botón X requiera múltiples clicks.
        """
        if not self.is_profile_drawer_open:
            # Cerrar el sidebar drawer (mobile) antes de abrir el profile drawer
            self.is_open = False
        self.is_profile_drawer_open = not self.is_profile_drawer_open

    @rx.event
    def set_profile_drawer_open(self, value: bool):
        """Abre o cierra el drawer de perfil (usado en on_open_change del drawer)."""
        self.is_profile_drawer_open = value

    @rx.event
    def toggle_auto_scroll(self):
        """Alterna el scroll automático"""
        self.auto_scroll_enabled = not self.auto_scroll_enabled
        print(f"[DEBUG] 🔄 Auto-scroll: {'activado' if self.auto_scroll_enabled else 'desactivado'}")
    
    @rx.event
    def clear_chat_history(self):
        """Limpia el historial del chat"""
        self.chat_history = []
        print("[DEBUG] 🧹 Historial del chat limpiado")
    
    @rx.event
    def update_user_info(self, name: str, email: str):
        """No-op, ya que Suplex maneja la información del usuario."""
        print(f"[DEBUG] 👤 Intentó actualizar info de usuario (manejado por Suplex): {name}")
    
    @rx.event
    def log_context_menu_open(self, is_open: bool):
        """Registra cuando se abre el menú contextual"""
        if is_open:
            print("[DEBUG] 📝 Context menu abierto")

    # === MÉTODOS DE GESTIÓN DE CONVERSACIONES OPTIMIZADOS ===
    @rx.event
    def reopen_drawer_if_needed(self):
        """Reabre el drawer solo si la bandera should_reopen_drawer es True"""
        if self.should_reopen_drawer:
            self.is_open = True
            self.should_reopen_drawer = False
            print("[DEBUG] 🔄 Drawer reabierto por bandera")

    @rx.event
    def open_edit_dialog(self, conversation_id: int, current_title: str):
        """
        Abre el diálogo de edición de título
        
        Args:
            conversation_id: ID de la conversación a editar
            current_title: Título actual de la conversación
        """
        print("[DEBUG] 📝 Opción seleccionada: Editar título")
        self.conversation_to_edit_id = conversation_id
        self.new_conversation_title = current_title
        self.is_edit_dialog_open = True
    
    @rx.event
    def close_edit_dialog(self):
        """Cierra el diálogo de edición"""
        self.is_edit_dialog_open = False
        self.conversation_to_edit_id = None
        self.new_conversation_title = ""
        print("[DEBUG] 📝 Diálogo de edición cerrado")
    
    @rx.event
    def save_conversation_title(self):
        """Guarda el nuevo título de la conversación de forma asíncrona"""
        if self.conversation_to_edit_id and self.new_conversation_title.strip():
            new_title = self.new_conversation_title.strip()
            
            # ⭐ USAR VERSIÓN ASÍNCRONA
            asyncio.create_task(self.update_conversation_title_async(
                self.conversation_to_edit_id,
                new_title
            ))
            
            print(f"[DEBUG] ✅ Título actualizado exitosamente a: {new_title}")
            self.close_edit_dialog()
    
    @rx.event
    def open_delete_dialog(self, conversation_id: int):
        """
        Abre el diálogo de confirmación de eliminación
        
        Args:
            conversation_id: ID de la conversación a eliminar
        """
        print("[DEBUG] 🗑️ Opción seleccionada: Eliminar conversación")
        self.conversation_to_delete_id = conversation_id
        self.is_delete_dialog_open = True

    @rx.event
    def close_delete_dialog(self):
        """Cierra el diálogo de eliminación"""
        self.is_delete_dialog_open = False
        self.conversation_to_delete_id = None
        print("[DEBUG] 🗑️ Diálogo de eliminación cerrado")

    @rx.event
    def confirm_delete_conversation(self):
        """Confirma la eliminación de la conversación de forma asíncrona"""
        if self.conversation_to_delete_id:
            # ⭐ USAR VERSIÓN ASÍNCRONA
            asyncio.create_task(self.delete_conversation_async(self.conversation_to_delete_id))
            
            # Si eliminamos la conversación actual, limpiar el chat
            if self.current_conversation_id == self.conversation_to_delete_id:
                self.chat_history = []
                print("[DEBUG] 🧹 Chat actual limpiado (conversación eliminada)")
            
            self.close_delete_dialog()
    
    # === MÉTODOS DE GESTIÓN DE CONVERSACIONES ASÍNCRONOS ===
    async def auto_generate_title_async(self, answer_text: str):
        """
        Genera automáticamente un título basado en la respuesta del asistente (async)
        
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
                    {"role": "system", "content": "Eres un experto creando títulos cortos y concisos para conversaciones. Responde solo con el título, sin comillas ni puntos."},
                    {"role": "user", "content": f"Crea un título muy breve (máximo 5 palabras) para una conversación sobre: {answer_text[:200]}"}
                ],
                max_tokens=15,
                temperature=0.5,
            )
            
            title = response.choices[0].message.content.strip()
            
            # Limpiar título
            title = title.replace('"', '').replace("'", "").strip()
            
            # Asegurar que no sea muy largo
            if len(title) > 40:
                title = title[:37] + "..."
            
            # ⭐ USAR VERSIÓN ASÍNCRONA PARA ACTUALIZAR
            await self.update_conversation_title_async(self.current_conversation_id, title)
            print(f"[DEBUG] 🤖 Título generado automáticamente: '{title}'")
            
        except Exception as e:
            print(f"[ERROR] ❌ Error generando título con IA: {e}")
            # Fallback: Usar primeros caracteres
            title = answer_text[:30] + "..." if len(answer_text) > 30 else answer_text
            await self.update_conversation_title_async(self.current_conversation_id, title)
    
    def start_new_conversation(self):
        """Inicia una nueva conversación limpiando el estado actual"""
        self.current_conversation_id = None
        self.current_thread_id = ""
        self.chat_history = []
        print("[DEBUG] 🆕 Nueva conversación iniciada")
    
    async def load_conversation_and_messages_async(self, conversation_id: int):
        """
        Carga una conversación y sus mensajes desde SUPABASE (local DB) de forma asíncrona
        
        Args:
            conversation_id: ID de la conversación a cargar
        """
        try:
            # ⭐ USAR VERSIÓN ASÍNCRONA OPTIMIZADA
            conversation = await self.load_conversation_by_id_async(conversation_id)
            
            if not conversation:
                print(f"[ERROR] ❌ No se encontró la conversación {conversation_id}")
                return
            
            print(f"[DEBUG] 🔄 Cambiando a conversación: '{conversation['title']}'")
            
            # Obtener mensajes de la BASE DE DATOS LOCAL
            messages_data = await self.get_messages_async(conversation_id)
            
            # Convertir a formato de chat_history
            new_history = []
            for msg in messages_data:
                new_history.append((msg["question"], msg["answer"]))
            
            self.chat_history = new_history
            print(f"[DEBUG] ✅ {len(new_history)} mensajes cargados desde Supabase")
            yield
            
        except Exception as e:
            print(f"[ERROR] ❌ Error cargando mensajes de la conversación: {e}")
    
    # ⭐ MANTENER MÉTODO COMPATIBLE
    async def load_conversation_and_messages(self, conversation_id: int):
        """Método compatible con la versión anterior"""
        async for _ in self.load_conversation_and_messages_async(conversation_id):
            pass
    
    # === MÉTODOS PARA DEBUG Y MONITOREO ===
    @rx.event
    def print_state_debug(self):
        """Imprime información de debug del estado"""
        print(f"[DEBUG] === ESTADO ACTUAL ===")
        print(f"  Conversaciones cargadas: {len(self.conversations)}")
        print(f"  Conversación actual ID: {self.current_conversation_id}")
        print(f"  Mensajes en chat: {len(self.chat_history)}")
        print(f"  Drawer abierto: {self.is_open}")
        print(f"  Drawer cargado: {self.drawer_loaded_once}")
        print(f"  Cache size: {len(self._conversations_cache) if hasattr(self, '_conversations_cache') else 'N/A'}")
        print(f"[DEBUG] ====================")
    
    # === MÉTODOS PARA MANEJO DE ERRORES ===
    @rx.event
    def clear_errors(self):
        """Limpia cualquier estado de error"""
        # Si hay un mensaje de error en el último chat, limpiarlo
        if self.chat_history and "⚠️" in self.chat_history[-1][1]:
            self.chat_history = self.chat_history[:-1]
            print("[DEBUG] 🧹 Error limpiado del chat")