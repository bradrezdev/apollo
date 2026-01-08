"""Estado de base de datos - Maneja todas las operaciones con la BD"""

import reflex as rx
from sqlmodel import Session, select
from db.conversations import Conversations
from db.engine import get_db_engine
from datetime import datetime, timezone


class DBState(rx.State):
    """Estado que maneja toda la lógica de base de datos"""
    
    # === VARIABLES DE CONVERSACIONES ===
    conversations: list[dict] = []
    current_conversation_id: int | None = None
    current_thread_id: str = ""
    is_loading_conversations: bool = False
    is_initial_load: bool = True  # Variable para controlar el splash screen
    
    # === MÉTODOS DE INICIALIZACIÓN ===
    def on_load(self):
        """Carga las conversaciones al iniciar la aplicación"""
        return self.load_conversations()
    
    # === MÉTODOS DE CONVERSACIONES ===
    def load_conversations(self):
        """Carga todas las conversaciones desde la base de datos ordenadas por fecha"""
        print("[DEBUG] Iniciando carga de conversaciones...", flush=True)
        
        self.is_loading_conversations = True
        yield
        
        try:
            engine = get_db_engine()
            print(f"[DEBUG] Conectando a BD con engine: {engine}", flush=True)
            with Session(engine) as session:
                statement = select(Conversations).order_by(Conversations.updated_at.desc())
                results = session.exec(statement).all()
                print(f"[DEBUG] Conversaciones encontradas en BD: {len(results)}", flush=True)
                
                # Convertir a diccionarios para el frontend
                self.conversations = [
                    {
                        "id": conv.id,
                        "thread_id": conv.thread_id,
                        "title": conv.title,
                        "created_at": conv.created_at.isoformat(),
                        "updated_at": conv.updated_at.isoformat(),
                    }
                    for conv in results
                ]
                print(f"[DEBUG] Conversaciones cargadas en estado: {len(self.conversations)}", flush=True)
            
            # Marcamos la carga inicial como completada
            self.is_initial_load = False
                
        except Exception as e:
            print(f"[ERROR] Error cargando conversaciones: {e}", flush=True)
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading_conversations = False
    
    def create_new_conversation(self, thread_id: str, title: str = "Nueva conversación") -> int | None:
        """
        Crea una nueva conversación en la base de datos
        
        Args:
            thread_id: ID del thread de OpenAI
            title: Título de la conversación (por defecto "Nueva conversación")
            
        Returns:
            ID de la conversación creada o None si hay error
        """
        print(f"[DEBUG] Creando nueva conversación. Thread ID: {thread_id}")
        try:
            with Session(get_db_engine()) as session:
                conversation = Conversations(
                    thread_id=thread_id,
                    title=title
                )
                session.add(conversation)
                session.commit()
                session.refresh(conversation)
                
                print(f"[DEBUG] Conversación creada exitosamente. ID: {conversation.id}")
                
                # Actualizar estado actual
                self.current_conversation_id = conversation.id
                self.current_thread_id = conversation.thread_id
                
                # Recargar lista de conversaciones (retornamos el generador para que Reflex lo maneje si es posible, 
                # aunque al ser llamado desde otro método puede que no se ejecute inmediatamente la parte del yield)
                # Para asegurar consistencia inmediata en variables, ya las seteamos arriba.
                # La actualización de la lista visual puede esperar.
                return conversation.id
                
        except Exception as e:
            print(f"[ERROR] Error creando conversación: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_conversation_by_id(self, conversation_id: int) -> dict | None:
        """
        Carga una conversación específica por su ID
        
        Args:
            conversation_id: ID de la conversación
            
        Returns:
            Diccionario con los datos de la conversación o None si no existe
        """
        try:
            with Session(Model.get_db_engine()) as session:
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
    
    def update_conversation_title(self, conversation_id: int, new_title: str):
        """
        Actualiza el título de una conversación
        
        Args:
            conversation_id: ID de la conversación
            new_title: Nuevo título
        """
        try:
            with Session(Model.get_db_engine()) as session:
                statement = select(Conversations).where(Conversations.id == conversation_id)
                conversation = session.exec(statement).first()
                
                if conversation:
                    conversation.title = new_title
                    conversation.updated_at = datetime.now(timezone.utc)
                    session.add(conversation)
                    session.commit()
                    
                    # Recargar lista de conversaciones
                    self.load_conversations()
                    
        except Exception as e:
            print(f"Error actualizando título: {e}")
    
    def update_conversation_timestamp(self, conversation_id: int):
        """
        Actualiza el timestamp de una conversación (para mantenerla al inicio de la lista)
        
        Args:
            conversation_id: ID de la conversación
        """
        try:
            with Session(Model.get_db_engine()) as session:
                statement = select(Conversations).where(Conversations.id == conversation_id)
                conversation = session.exec(statement).first()
                
                if conversation:
                    conversation.updated_at = datetime.now(timezone.utc)
                    session.add(conversation)
                    session.commit()
                    
        except Exception as e:
            print(f"Error actualizando timestamp: {e}")
    
    def delete_conversation(self, conversation_id: int):
        """
        Elimina una conversación de la base de datos
        
        Args:
            conversation_id: ID de la conversación a eliminar
        """
        try:
            with Session(Model.get_db_engine()) as session:
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
                    
                    # Recargar lista de conversaciones
                    self.load_conversations()
                    
        except Exception as e:
            print(f"Error eliminando conversación: {e}")
    
    # === MÉTODOS AUXILIARES ===
    def get_current_conversation(self) -> dict | None:
        """
        Obtiene la conversación actual desde la lista cargada
        
        Returns:
            Diccionario con los datos de la conversación actual o None
        """
        if self.current_conversation_id:
            for conv in self.conversations:
                if conv["id"] == self.current_conversation_id:
                    return conv
        return None
