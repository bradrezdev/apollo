"""Estado de base de datos - Maneja todas las operaciones con la BD"""

import reflex as rx
from sqlmodel import Session, select, text
from Proyecto_Apollo.models.conversations import Conversations
from Proyecto_Apollo.models.messages import Messages
from Proyecto_Apollo.models.users import Users
# engine removed
from datetime import datetime, timezone
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading

# ⭐⭐ ThreadPool para operaciones de base de datos
_db_executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="db_worker")

from Proyecto_Apollo.modules.auth.state.auth_state import AuthState

class DBState(AuthState):
    """Estado optimizado que maneja toda la lógica de base de datos de forma asíncrona"""
    
    # === VARIABLES DE CONVERSACIONES ===
    conversations: list[dict] = []
    current_conversation_id: int | None = None
    current_thread_id: str = ""
    is_loading_conversations: bool = False
    is_initial_load: bool = True  # Variable para controlar el splash screen
    
    # === NUEVAS VARIABLES PARA OPTIMIZACIÓN ===
    _conversations_cache: dict[int, dict] = {}  # Cache en memoria
    _last_conversations_load: datetime | None = None
    _conversations_loaded: bool = False

    # local_user_id se hereda de AuthState (declarado allí para que submit_login
    # y submit_step3 puedan setearlo sin violar la restricción de Reflex).
    
    def sync_user_sync(self):
        """Sincroniza el usuario de Supabase Auth con la base de datos local.
        
        Usa get_user() (llamada HTTP) en lugar de self.user_id (JWT decode)
        porque el proyecto usa ECC P-256 y el decode HS256 siempre falla.
        """
        if not self.access_token:
            return None
            
        try:
            # Obtener datos del usuario via API (no depende de JWT decode)
            user_data = self.get_user()
            if not user_data:
                return None
                
            supabase_uid = user_data.get("id")
            user_email = user_data.get("email", "")
            meta = user_data.get("user_metadata") or {}
            first_name = meta.get("first_name", "")
            last_name = meta.get("last_name", "")
            
            if not supabase_uid:
                return None
                
            with rx.session() as session:
                statement = select(Users).where(Users.supabase_uid == supabase_uid)
                user = session.exec(statement).first()
                if user:
                    return user.id
                
                # Crear nuevo usuario si no existe
                new_user = Users(
                    supabase_uid=supabase_uid,
                    correo=user_email,
                    nombre=first_name,
                    apellido=last_name,
                    fecha_de_nacimiento="N/A",
                    password_hash="supabase_managed",
                    salt="N/A",
                    bo_connection=False,
                )
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                print(f"[DEBUG] 👤 Usuario sincronizado localmente con ID: {new_user.id}")
                return new_user.id
        except Exception as e:
            print(f"[ERROR] ❌ Error sincronizando usuario: {e}")
            return None

    
    # === MÉTODOS DE INICIALIZACIÓN ASÍNCRONOS ===
    async def on_load(self):
        """Carga las conversaciones al iniciar la aplicación de forma asíncrona"""
        async for _ in self.load_conversations_async():
            pass

    # === MÉTODOS ASÍNCRONOS OPTIMIZADOS ===
    async def load_conversations_async(self):
        """
        Carga todas las conversaciones desde la base de datos de forma ASÍNCRONA
        No bloquea el thread principal - ideal para UI
        """
        print("[DEBUG] 🔄 Iniciando carga ASÍNCRONA de conversaciones...", flush=True)
        
        # Si ya estamos cargando, no hacer nada
        if self.is_loading_conversations:
            return
        
        # Si ya cargamos recientemente (menos de 30 segundos), usar cache
        if (self._conversations_loaded and 
            self._last_conversations_load and 
            (datetime.now(timezone.utc) - self._last_conversations_load).total_seconds() < 30):
            print("[DEBUG] ✅ Usando cache de conversaciones (carga reciente)", flush=True)
            return
        
        self.is_loading_conversations = True
        yield  # ⭐ Permitir que UI muestre spinner inmediatamente
        
        try:
            # Sincronizar usuario antes de cargar
            if not self.local_user_id:
                self.local_user_id = self.sync_user_sync()
            
            # ⭐ Ejecutar en thread separado para no bloquear
            loop = asyncio.get_event_loop()
            conversations_data = await loop.run_in_executor(
                _db_executor,
                self._load_conversations_sync,
                self.local_user_id
            )
            
            if conversations_data:
                # Actualizar cache
                self.conversations = conversations_data
                self._update_conversations_cache(conversations_data)
                self._conversations_loaded = True
                self._last_conversations_load = datetime.now(timezone.utc)
                
                print(f"[DEBUG] ✅ {len(self.conversations)} conversaciones cargadas async", flush=True)
            
            # Marcamos la carga inicial como completada
            self.is_initial_load = False
                
        except Exception as e:
            print(f"[ERROR] ❌ Error cargando conversaciones async: {e}", flush=True)
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading_conversations = False
            yield
    
    def _load_conversations_sync(self, user_id: int | None = None) -> list[dict]:
        """
        Método síncrono que se ejecuta en thread separado
        Contiene toda la lógica pesada de base de datos
        """
        try:
            start_time = datetime.now(timezone.utc)
            
            print(f"[DEBUG] 🔌 Conectando a BD", flush=True)
            
            with rx.session() as session:
                # ⭐ CONSULTA OPTIMIZADA CON ÍNDICE
                statement = select(Conversations)
                if user_id:
                    statement = statement.where(Conversations.user_id == user_id)
                statement = statement.order_by(Conversations.updated_at.desc())
                results = session.exec(statement).all()
                
                query_time = (datetime.now(timezone.utc) - start_time).total_seconds()
                print(f"[DEBUG] ⚡ Consulta ejecutada en {query_time:.3f} segundos", flush=True)
                print(f"[DEBUG] 📊 Conversaciones encontradas en BD: {len(results)}", flush=True)
                
                # ⭐ CONVERSIÓN OPTIMIZADA A DICTS
                conversations_list = []
                for conv in results:
                    conversations_list.append({
                        "id": conv.id,
                        "thread_id": conv.thread_id,
                        "title": conv.title,
                        "created_at": conv.created_at,  # Mantener datetime
                        "updated_at": conv.updated_at,   # Mantener datetime
                    })
                
                total_time = (datetime.now(timezone.utc) - start_time).total_seconds()
                print(f"[DEBUG] ⏱️  Tiempo total carga síncrona: {total_time:.3f}s", flush=True)
                
                return conversations_list
                
        except Exception as e:
            print(f"[ERROR] ❌ Error en carga síncrona: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return []
    
    def _update_conversations_cache(self, conversations_list: list[dict]):
        """Actualiza el cache en memoria para búsquedas rápidas"""
        self._conversations_cache.clear()
        for conv in conversations_list:
            self._conversations_cache[conv["id"]] = conv
    
    # === MÉTODO COMPATIBLE (para mantener integración) ===
    def load_conversations(self):
        """
        Método original mantenido para compatibilidad
        Redirige al método asíncrono
        """
        return self.load_conversations_async()
    
    # === MÉTODOS DE CRUD OPTIMIZADOS ===
    async def create_new_conversation_async(self, thread_id: str, title: str = "Nueva conversación") -> int | None:
        """
        Crea una nueva conversación de forma asíncrona
        
        Args:
            thread_id: ID del thread de OpenAI
            title: Título de la conversación
            
        Returns:
            ID de la conversación creada o None si hay error
        """
        print(f"[DEBUG] 🆕 Creando nueva conversación async. Thread ID: {thread_id}", flush=True)
        
        try:
            # Ejecutar en thread separado
            loop = asyncio.get_event_loop()
            
            if not self.local_user_id:
                self.local_user_id = self.sync_user_sync()
                
            conversation_id = await loop.run_in_executor(
                _db_executor,
                self._create_conversation_sync,
                thread_id,
                title,
                self.local_user_id
            )
            
            if conversation_id:
                # Recargar lista después de crear (en background)
                asyncio.create_task(self._reload_conversations_background())
                
            return conversation_id
                
        except Exception as e:
            print(f"[ERROR] ❌ Error creando conversación async: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return None
    
    def _create_conversation_sync(self, thread_id: str, title: str, user_id: int | None = None) -> int | None:
        """Método síncrono para crear conversación"""
        try:
            with rx.session() as session:
                conversation = Conversations(
                    thread_id=thread_id,
                    title=title,
                    user_id=user_id
                )
                session.add(conversation)
                session.commit()
                session.refresh(conversation)
                
                print(f"[DEBUG] ✅ Conversación creada exitosamente. ID: {conversation.id}", flush=True)
                
                # Actualizar estado actual inmediatamente
                self.current_conversation_id = conversation.id
                self.current_thread_id = conversation.thread_id
                
                return conversation.id
                
        except Exception as e:
            print(f"[ERROR] ❌ Error creando conversación sync: {e}", flush=True)
            return None
    
    async def _reload_conversations_background(self):
        """Recarga conversaciones en segundo plano sin bloquear"""
        try:
            if not self.is_loading_conversations:
                async for _ in self.load_conversations_async():
                    pass
        except Exception as e:
            print(f"[DEBUG] ℹ️  Error en recarga background: {e}", flush=True)
    
    def create_new_conversation(self, thread_id: str, title: str = "Nueva conversación") -> int | None:
        """Método compatible para creación síncrona (mantener para compatibilidad)"""
        # Nota: Este método bloquea. Mejor usar create_new_conversation_async
        try:
            with rx.session() as session:
                conversation = Conversations(
                    thread_id=thread_id,
                    title=title,
                    user_id=self.local_user_id
                )
                session.add(conversation)
                session.commit()
                session.refresh(conversation)
                
                print(f"[DEBUG] Conversación creada exitosamente. ID: {conversation.id}")
                
                self.current_conversation_id = conversation.id
                self.current_thread_id = conversation.thread_id
                
                # Recargar en background sin bloquear
                asyncio.create_task(self._reload_conversations_background())
                
                return conversation.id
                
        except Exception as e:
            print(f"[ERROR] Error creando conversación: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    # === MÉTODOS OPTIMIZADOS CON CACHE ===
    async def load_conversation_by_id_async(self, conversation_id: int) -> dict | None:
        """
        Carga una conversación específica por su ID usando cache primero
        
        Args:
            conversation_id: ID de la conversación
            
        Returns:
            Diccionario con los datos de la conversación o None si no existe
        """
        # ⭐ PRIMERO: Buscar en cache
        if conversation_id in self._conversations_cache:
            print(f"[DEBUG] 🏎️  Conversación {conversation_id} encontrada en cache", flush=True)
            return self._conversations_cache[conversation_id]
        
        # ⭐ SEGUNDO: Buscar en base de datos (async)
        try:
            loop = asyncio.get_event_loop()
            conversation = await loop.run_in_executor(
                _db_executor,
                self._load_conversation_by_id_sync,
                conversation_id
            )
            
            if conversation:
                # Actualizar cache
                self._conversations_cache[conversation_id] = conversation
                
                # Actualizar estado
                self.current_conversation_id = conversation["id"]
                self.current_thread_id = conversation["thread_id"]
            
            return conversation
            
        except Exception as e:
            print(f"[ERROR] ❌ Error cargando conversación async: {e}", flush=True)
            return None
    
    def _load_conversation_by_id_sync(self, conversation_id: int) -> dict | None:
        """Método síncrono para cargar conversación por ID"""
        try:
            with rx.session() as session:
                statement = select(Conversations).where(Conversations.id == conversation_id)
                conversation = session.exec(statement).first()
                
                if conversation:
                    return {
                        "id": conversation.id,
                        "thread_id": conversation.thread_id,
                        "title": conversation.title,
                        "created_at": conversation.created_at,
                        "updated_at": conversation.updated_at,
                    }
                return None
                
        except Exception as e:
            print(f"[ERROR] ❌ Error cargando conversación sync: {e}", flush=True)
            return None
    
    # Mantener método compatible
    def load_conversation_by_id(self, conversation_id: int) -> dict | None:
        """Método original mantenido para compatibilidad"""
        # Primero buscar en cache
        if conversation_id in self._conversations_cache:
            conv = self._conversations_cache[conversation_id]
            self.current_conversation_id = conv["id"]
            self.current_thread_id = conv["thread_id"]
            return conv
        
        # Si no está en cache, cargar síncronamente (puede bloquear)
        try:
            with rx.session() as session:
                statement = select(Conversations).where(Conversations.id == conversation_id)
                conversation = session.exec(statement).first()
                
                if conversation:
                    self.current_conversation_id = conversation.id
                    self.current_thread_id = conversation.thread_id
                    
                    return {
                        "id": conversation.id,
                        "thread_id": conversation.thread_id,
                        "title": conversation.title,
                        "created_at": conversation.created_at.isoformat(),
                        "updated_at": conversation.updated_at.isoformat(),
                    }
                return None
                
        except Exception as e:
            print(f"Error cargando conversación: {e}")
            return None
    
    # === MÉTODOS DE ACTUALIZACIÓN OPTIMIZADOS ===
    async def update_conversation_title_async(self, conversation_id: int, new_title: str):
        """
        Actualiza el título de una conversación de forma asíncrona
        
        Args:
            conversation_id: ID de la conversación
            new_title: Nuevo título
        """
        print(f"[DEBUG] 📝 Actualizando título async para conversación {conversation_id}", flush=True)
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                _db_executor,
                self._update_conversation_title_sync,
                conversation_id,
                new_title
            )
            
            # Actualizar cache
            if conversation_id in self._conversations_cache:
                self._conversations_cache[conversation_id]["title"] = new_title
                self._conversations_cache[conversation_id]["updated_at"] = datetime.now(timezone.utc)
            
            # Recargar lista en background
            asyncio.create_task(self._reload_conversations_background())
            
        except Exception as e:
            print(f"[ERROR] ❌ Error actualizando título async: {e}", flush=True)
    
    def _update_conversation_title_sync(self, conversation_id: int, new_title: str):
        """Método síncrono para actualizar título"""
        try:
            with rx.session() as session:
                statement = select(Conversations).where(Conversations.id == conversation_id)
                conversation = session.exec(statement).first()
                
                if conversation:
                    conversation.title = new_title
                    conversation.updated_at = datetime.now(timezone.utc)
                    session.add(conversation)
                    session.commit()
                    
        except Exception as e:
            print(f"[ERROR] ❌ Error actualizando título sync: {e}", flush=True)
            raise
    
    # Mantener método compatible
    def update_conversation_title(self, conversation_id: int, new_title: str):
        """Método original mantenido para compatibilidad"""
        try:
            with rx.session() as session:
                statement = select(Conversations).where(Conversations.id == conversation_id)
                conversation = session.exec(statement).first()
                
                if conversation:
                    conversation.title = new_title
                    conversation.updated_at = datetime.now(timezone.utc)
                    session.add(conversation)
                    session.commit()
                    
                    # Recargar lista de conversaciones en background
                    asyncio.create_task(self._reload_conversations_background())
                    
        except Exception as e:
            print(f"Error actualizando título: {e}")
    
    async def update_conversation_timestamp_async(self, conversation_id: int):
        """
        Actualiza el timestamp de una conversación de forma asíncrona
        
        Args:
            conversation_id: ID de la conversación
        """
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                _db_executor,
                self._update_conversation_timestamp_sync,
                conversation_id
            )
            
            # Actualizar cache
            if conversation_id in self._conversations_cache:
                self._conversations_cache[conversation_id]["updated_at"] = datetime.now(timezone.utc)
            
        except Exception as e:
            print(f"[ERROR] ❌ Error actualizando timestamp async: {e}", flush=True)
    
    def _update_conversation_timestamp_sync(self, conversation_id: int):
        """Método síncrono para actualizar timestamp"""
        try:
            with rx.session() as session:
                statement = select(Conversations).where(Conversations.id == conversation_id)
                conversation = session.exec(statement).first()
                
                if conversation:
                    conversation.updated_at = datetime.now(timezone.utc)
                    session.add(conversation)
                    session.commit()
                    
        except Exception as e:
            print(f"[ERROR] ❌ Error actualizando timestamp sync: {e}", flush=True)
            raise
    
    # Mantener método compatible
    def update_conversation_timestamp(self, conversation_id: int):
        """Método original mantenido para compatibilidad"""
        try:
            with rx.session() as session:
                statement = select(Conversations).where(Conversations.id == conversation_id)
                conversation = session.exec(statement).first()
                
                if conversation:
                    conversation.updated_at = datetime.now(timezone.utc)
                    session.add(conversation)
                    session.commit()
                    
        except Exception as e:
            print(f"Error actualizando timestamp: {e}")
    
    # === MÉTODOS DE ELIMINACIÓN OPTIMIZADOS ===
    async def delete_conversation_async(self, conversation_id: int):
        """
        Elimina una conversación de forma asíncrona
        
        Args:
            conversation_id: ID de la conversación a eliminar
        """
        print(f"[DEBUG] 🗑️  Eliminando conversación async: {conversation_id}", flush=True)
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                _db_executor,
                self._delete_conversation_sync,
                conversation_id
            )
            
            # Limpiar cache
            if conversation_id in self._conversations_cache:
                del self._conversations_cache[conversation_id]
            
            # Si era la conversación actual, limpiar estado
            if self.current_conversation_id == conversation_id:
                self.current_conversation_id = None
                self.current_thread_id = ""
            
            # Recargar lista en background
            asyncio.create_task(self._reload_conversations_background())
            
        except Exception as e:
            print(f"[ERROR] ❌ Error eliminando conversación async: {e}", flush=True)
    
    def _delete_conversation_sync(self, conversation_id: int):
        """Método síncrono para eliminar conversación"""
        try:
            with rx.session() as session:
                statement = select(Conversations).where(Conversations.id == conversation_id)
                conversation = session.exec(statement).first()
                
                if conversation:
                    title = conversation.title
                    session.delete(conversation)
                    session.commit()
                    print(f"[DEBUG] ✅ Conversación eliminada exitosamente: {title}", flush=True)
                    
        except Exception as e:
            print(f"[ERROR] ❌ Error eliminando conversación sync: {e}", flush=True)
            raise
    
    # Mantener método compatible
    def delete_conversation(self, conversation_id: int):
        """Método original mantenido para compatibilidad"""
        try:
            with rx.session() as session:
                statement = select(Conversations).where(Conversations.id == conversation_id)
                conversation = session.exec(statement).first()
                
                if conversation:
                    title = conversation.title
                    session.delete(conversation)
                    session.commit()
                    print(f"[DEBUG] Conversacion eliminada exitosamente: {title}")
                    
                    # Si era la conversación actual, limpiar estado
                    if self.current_conversation_id == conversation_id:
                        self.current_conversation_id = None
                        self.current_thread_id = ""
                    
                    # Recargar lista de conversaciones en background
                    asyncio.create_task(self._reload_conversations_background())
                    
        except Exception as e:
            print(f"Error eliminando conversación: {e}")
    
    # === MÉTODOS AUXILIARES OPTIMIZADOS ===
    def get_current_conversation(self) -> dict | None:
        """
        Obtiene la conversación actual desde el CACHE (rápido)
        
        Returns:
            Diccionario con los datos de la conversación actual o None
        """
        if self.current_conversation_id:
            return self._conversations_cache.get(self.current_conversation_id)
        return None
    
    # === MÉTODOS PARA GESTIÓN DE CACHE ===
    def invalidate_cache(self):
        """Invalida el cache de conversaciones para forzar recarga"""
        self._conversations_cache.clear()
        self._conversations_loaded = False
        self._last_conversations_load = None
        print("[DEBUG] 🧹 Cache de conversaciones invalidado", flush=True)
    
    async def refresh_conversations(self):
        """Fuerza una recarga completa de conversaciones"""
        self.invalidate_cache()
        await self.load_conversations_async()
    
    # === UTILIDADES PARA DEBUG ===
    @rx.var
    def cache_stats(self) -> dict:
        """Estadísticas del cache para debug"""
        return {
            "cache_size": len(self._conversations_cache),
            "conversations_count": len(self.conversations),
            "last_load": self._last_conversations_load.isoformat() if self._last_conversations_load else None,
            "is_loaded": self._conversations_loaded,
        }

    # === GESTIÓN DE MENSAJES ===

    def add_message(self, conversation_id: int, question: str, answer: str):
        """Guarda un mensaje en la base de datos (Síncrono para ThreadPool)"""
        with rx.session() as session:
            message = Messages(
                conversation_id=conversation_id,
                question_encrypted=question,
                answer_encrypted=answer
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            print(f"[DEBUG] Mensaje guardado en BD id={message.id}", flush=True)
            return message

    async def add_message_async(self, conversation_id: int, question: str, answer: str):
        """Guarda un mensaje de forma asíncrona"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            _db_executor,  # Usar la variable global directamente
            self.add_message, 
            conversation_id, 
            question, 
            answer
        )

    def get_messages(self, conversation_id: int) -> list[dict]:
        """Obtiene mensajes de una conversación (Síncrono)"""
        with rx.session() as session:
            statement = select(Messages).where(
                Messages.conversation_id == conversation_id
            ).order_by(Messages.created_at)
            results = session.exec(statement).all()
            return [
                {
                    "question": msg.question_encrypted, 
                    "answer": msg.answer_encrypted, 
                    "created_at": msg.created_at
                } 
                for msg in results
            ]

    async def get_messages_async(self, conversation_id: int) -> list[dict]:
        """Obtiene mensajes de forma asíncrona"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            _db_executor,
            self.get_messages,
            conversation_id
        )

# ⭐⭐ PRECALENTAMIENTO DEL ENGINE EN BACKGROUND
def warmup_database_connection():
    """Precalienta la conexión a la base de datos en segundo plano"""
    print("[DEBUG] 🔥 Precalentando conexión a BD en background...", flush=True)
    try:
        # Solo crear una conexión simple para activar el pool
        with rx.session() as session:
            # Usar text() para consultas SQL crudas
            session.execute(text("SELECT 1"))
        print("[DEBUG] ✅ Conexión precalentada", flush=True)
    except Exception as e:
        print(f"[DEBUG] ℹ️  Nota: Precalentamiento falló (puede ser normal): {e}", flush=True)

# Iniciar precalentamiento al importar el módulo
warmup_thread = threading.Thread(
    target=warmup_database_connection,
    daemon=True,
    name="DB-Warmup-Thread"
)
warmup_thread.start()