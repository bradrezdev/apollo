"""
Sistema de cola para registros - Alternativa simple

Este módulo proporciona dos enfoques:
1. RegistrationQueue: Sistema completo con threading para bulk registration
2. sign_up_with_delay: Función simple con delay para evitar rate limiting

Uso:
    # Enfoque simple (recomendado para flujos normales):
    from Proyecto_Apollo.modules.auth.backend.queue_helpers import sign_up_with_delay
    success, msg, uid = sign_up_with_delay(email, password, first_name, last_name)
    
    # Enfoque cola (para múltiples registros):
    from Proyecto_Apollo.background_tasks import registration_queue
    registration_queue.enqueue_registration({...})
"""

import time
import random
import threading
import logging
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# Configuración global de delays
MIN_DELAY = 2.0
MAX_DELAY = 5.0
MAX_ATTEMPTS = 3


def sign_up_with_delay(
    email: str,
    password: str,
    first_name: str = "",
    last_name: str = "",
    min_delay: float = MIN_DELAY,
    max_delay: float = MAX_DELAY
) -> Tuple[bool, str, Optional[str]]:
    """
    Registra un usuario con delay aleatorio para evitar rate limiting.
    
    Args:
        email: Email del usuario
        password: Contraseña
        first_name: Nombre
        last_name: Apellido
        min_delay: Delay mínimo en segundos
        max_delay: Delay máximo en segundos
        
    Returns:
        Tupla (success, message, user_id)
    """
    from suplex import Suplex
    
    delay = random.uniform(min_delay, max_delay)
    logger.info(f"[sign_up_with_delay] Esperando {delay:.1f}s antes de registrar {email}")
    time.sleep(delay)
    
    try:
        suplex = Suplex()
        response = suplex.sign_up(
            email=email.strip(),
            password=password.strip(),
            options={
                "data": {
                    "first_name": first_name.strip(),
                    "last_name": last_name.strip()
                }
            }
        )
        
        if response and response.user:
            return True, "Usuario creado exitosamente", response.user.id
        return False, "Error al crear usuario", None
        
    except Exception as e:
        error_msg = str(e).lower()
        if "user already registered" in error_msg or "already been registered" in error_msg:
            return False, "El email ya está registrado", None
        elif "password" in error_msg:
            return False, "La contraseña no cumple con los requisitos", None
        elif "email" in error_msg:
            return False, "Email inválido", None
        return False, f"Error de registro: {str(e)}", None


def bulk_sign_up(
    users: List[Dict[str, str]],
    on_progress: Optional[callable] = None
) -> List[Dict[str, Any]]:
    """
    Registra múltiples usuarios con delays entre cada uno.
    
    Args:
        users: Lista de diccionarios con keys: email, password, first_name, last_name
        on_progress: Callback opcional (index, total, result) para progreso
        
    Returns:
        Lista de resultados con email, success, user_id, error
    """
    results = []
    total = len(users)
    
    for i, user in enumerate(users):
        logger.info(f"[bulk_sign_up] Registrando {i+1}/{total}: {user.get('email')}")
        
        success, msg, uid = sign_up_with_delay(
            email=user.get("email", ""),
            password=user.get("password", ""),
            first_name=user.get("first_name", ""),
            last_name=user.get("last_name", "")
        )
        
        result = {
            "email": user.get("email"),
            "success": success,
            "user_id": uid,
            "message": msg
        }
        results.append(result)
        
        if on_progress:
            on_progress(i + 1, total, result)
    
    return results


# Re-exportar la cola principal
from Proyecto_Apollo.background_tasks import (
    registration_queue,
    RegistrationQueue,
    get_queue_status,
    enqueue_user_registration
)

__all__ = [
    "sign_up_with_delay",
    "bulk_sign_up",
    "registration_queue",
    "RegistrationQueue",
    "get_queue_status",
    "enqueue_user_registration"
]
