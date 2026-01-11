"""Configuración de API Keys y constantes de la aplicación"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# === OPENAI CONFIGURATION ===
# NOTA: Hardcoded por solicitud explícita para despliegue
OPENAI_API_KEY = "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"
API_ASSISTANT_ID = "asst_wbg01t4JFYx0AVal09mtljlS"


# === SUPABASE CONFIGURATION ===
# Valores hardcoded
SUPABASE_URL = "https://mqajbtjxwdtwimoavhjz.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xYWpidGp4d2R0d2ltb2F2aGp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgwNDg4NzUsImV4cCI6MjA2MzYyNDg3NX0.JvgIf5-4Xuxef-bQi6JgFHI0CbdpiOouI654cxqwMQo"
DATABASE_URL = "postgresql://postgres:project_apollo@db.xtcoumbygvhdwakxduvw.supabase.co:5432/postgres"

# === APP CONFIGURATION ===
APP_NAME = "Proyecto_Apollo"
APP_DESCRIPTION = "Chatbot con IA usando OpenAI Assistants"
