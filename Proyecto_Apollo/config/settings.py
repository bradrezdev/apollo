"""Configuración de API Keys y constantes de la aplicación"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# === OPENAI CONFIGURATION ===
# Cargar desde variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_ASSISTANT_ID = os.getenv("API_ASSISTANT_ID")


# === SUPABASE CONFIGURATION ===
# Cargar desde variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# === APP CONFIGURATION ===
APP_NAME = "Proyecto_Apollo"
APP_DESCRIPTION = "Chatbot con IA usando OpenAI Assistants"