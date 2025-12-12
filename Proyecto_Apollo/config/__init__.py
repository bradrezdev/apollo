"""__init__.py para configuración"""

from .settings import (
    OPENAI_API_KEY,
    API_ASSISTANT_ID,
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    APP_NAME,
    APP_DESCRIPTION,
)

__all__ = [
    "OPENAI_API_KEY",
    "API_ASSISTANT_ID",
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY",
    "APP_NAME",
    "APP_DESCRIPTION",
]
