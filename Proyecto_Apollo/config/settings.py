"""Configuración de API Keys y constantes de la aplicación"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# === OPENAI CONFIGURATION ===
# Hardcoded para producción ya que Reflex Cloud no soporta secrets
OPENAI_API_KEY = "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"
API_ASSISTANT_ID = "asst_tvVa2SUaRhesqjphWE09I7Wx"

# === SUPABASE CONFIGURATION ===
SUPABASE_URL = "https://mqajbtjxwdtwimoavhjz.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xYWpidGp4d2R0d2ltb2F2aGp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgwNDg4NzUsImV4cCI6MjA2MzYyNDg3NX0.JvgIf5-4Xuxef-bQi6JgFHI0CbdpiOouI654cxqwMQo"

# === APP CONFIGURATION ===
APP_NAME = "Proyecto Apollo"
APP_DESCRIPTION = "Chatbot con IA usando OpenAI Assistants"
