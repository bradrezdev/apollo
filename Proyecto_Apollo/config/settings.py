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
# SUPABASE_JWT_SECRET no es necesario: el proyecto usa JWT Keys ECC (P-256).
# Suplex decodifica access_tokens via JWKS automáticamente cuando jwt_secret no está en config.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///reflex.db")

# === APP CONFIGURATION ===
APP_NAME = "Proyecto_Apollo"
APP_DESCRIPTION = "Chatbot con IA usando OpenAI Assistants"
APP_VERSION = "1.0"