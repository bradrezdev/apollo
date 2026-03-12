"""
Background Tasks - Registration Queue System

Sistema de cola para procesar registros de usuarios en background
y evitar rate limiting de Supabase.

Uso:
    from Proyecto_Apollo.modules.auth.backend.background_tasks import (
        registration_queue, 
        RegistrationQueue,
        get_queue_status
    )
    
    # Encolar un registro:
    registration_queue.enqueue_registration({
        "email": "user@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe"
    })
    
    # Consultar estado de la cola:
    status = get_queue_status()
"""

import threading
import time
import random
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueueStatus(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    PAUSED = "paused"


@dataclass
class QueueItem:
    """Elemento en la cola de registro."""
    id: str
    user_data: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    attempts: int = 0


class RegistrationQueue:
    """Cola de registros con procesamiento en background."""

    def __init__(
        self,
        min_delay: float = 2.0,
        max_delay: float = 5.0,
        max_attempts: int = 3
    ):
        self._queue: List[QueueItem] = []
        self._lock = threading.Lock()
        self._worker_thread: Optional[threading.Thread] = None
        self._running = False
        self._status = QueueStatus.IDLE

        self.min_delay = min_delay
        self.max_delay = max_delay
        self.max_attempts = max_attempts

        self._on_complete: Optional[callable] = None
        self._on_error: Optional[callable] = None

    def start(self):
        """Inicia el worker de procesamiento."""
        if self._running:
            return
        self._running = True
        self._worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self._worker_thread.start()
        logger.info("[RegistrationQueue] Worker iniciado")

    def stop(self):
        """Detiene el worker de procesamiento."""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=5)
        logger.info("[RegistrationQueue] Worker detenido")

    def enqueue_registration(self, user_data: Dict[str, Any]) -> str:
        """Agrega un registro a la cola."""
        item_id = f"reg_{len(self._queue)}_{int(time.time() * 1000)}"
        item = QueueItem(id=item_id, user_data=user_data)

        with self._lock:
            self._queue.append(item)
            logger.info(f"[RegistrationQueue] Encolado: {user_data.get('email', 'unknown')}")

        if not self._running:
            self.start()

        return item_id

    def _process_queue(self):
        """Worker que procesa la cola en background."""
        while self._running:
            item = None

            with self._lock:
                for q_item in self._queue:
                    if q_item.status == "pending":
                        item = q_item
                        item.status = "processing"
                        break

            if item is None:
                time.sleep(1)
                continue

            self._status = QueueStatus.PROCESSING
            logger.info(f"[RegistrationQueue] Procesando: {item.user_data.get('email', 'unknown')}")

            try:
                result = self._process_registration(item.user_data)
                item.status = "completed"
                item.result = result
                logger.info(f"[RegistrationQueue] Completado: {item.user_data.get('email', 'unknown')}")

                if self._on_complete:
                    self._on_complete(item)

            except Exception as e:
                item.attempts += 1
                if item.attempts < self.max_attempts:
                    item.status = "pending"
                    logger.warning(f"[RegistrationQueue] Reintentando ({item.attempts}/{self.max_attempts}): {e}")
                else:
                    item.status = "failed"
                    item.error = str(e)
                    logger.error(f"[RegistrationQueue] Fallido: {e}")

                    if self._on_error:
                        self._on_error(item)

            delay = random.uniform(self.min_delay, self.max_delay)
            logger.info(f"[RegistrationQueue] Esperando {delay:.1f}s antes del siguiente...")
            time.sleep(delay)

            with self._lock:
                pending_count = sum(1 for q in self._queue if q.status == "pending")
                if pending_count == 0:
                    self._status = QueueStatus.IDLE

    def _process_registration(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa el registro real en Supabase."""
        from suplex import Suplex

        suplex = Suplex()

        try:
            response = suplex.sign_up(
                email=user_data["email"].strip(),
                password=user_data["password"].strip(),
                options={
                    "data": {
                        "first_name": user_data.get("first_name", "").strip(),
                        "last_name": user_data.get("last_name", "").strip()
                    }
                }
            )
            return {"success": True, "user_id": response.user.id if response else None}
        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}")

    def get_status(self) -> Dict[str, Any]:
        """Retorna el estado actual de la cola."""
        with self._lock:
            pending = sum(1 for q in self._queue if q.status == "pending")
            processing = sum(1 for q in self._queue if q.status == "processing")
            completed = sum(1 for q in self._queue if q.status == "completed")
            failed = sum(1 for q in self._queue if q.status == "failed")

        return {
            "status": self._status.value,
            "queue_size": len(self._queue),
            "pending": pending,
            "processing": processing,
            "completed": completed,
            "failed": failed,
            "running": self._running
        }

    def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un item específico de la cola."""
        with self._lock:
            for item in self._queue:
                if item.id == item_id:
                    return {
                        "id": item.id,
                        "email": item.user_data.get("email"),
                        "status": item.status,
                        "result": item.result,
                        "error": item.error,
                        "attempts": item.attempts,
                        "created_at": item.created_at.isoformat()
                    }
        return None

    def clear_completed(self):
        """Limpia items completados de la cola."""
        with self._lock:
            self._queue = [q for q in self._queue if q.status not in ("completed", "failed")]
            logger.info("[RegistrationQueue] Limpiados items completados")

    def set_callbacks(self, on_complete: callable = None, on_error: callable = None):
        """Configura callbacks para eventos de la cola."""
        self._on_complete = on_complete
        self._on_error = on_error


registration_queue = RegistrationQueue(min_delay=2.0, max_delay=5.0)


def get_queue_status() -> Dict[str, Any]:
    """Función de conveniencia para obtener el estado de la cola."""
    return registration_queue.get_status()


def enqueue_user_registration(user_data: Dict[str, Any]) -> str:
    """Función de conveniencia para encolar un registro."""
    return registration_queue.enqueue_registration(user_data)
