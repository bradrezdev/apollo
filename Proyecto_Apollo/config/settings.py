"""Configuración de API Keys y constantes de la aplicación"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# === OPENAI CONFIGURATION ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-i1UmS_YTnDZrqlh2P_BzutHN2Cs5Em1_v9Ansvdek_T3BlbkFJz4pHhL_L8aL2IvExcf0h-_Sl7dOujDyyKUmMsddNUA")
API_ASSISTANT_ID = os.getenv("API_ASSISTANT_ID", "asst_tvVa2SUaRhesqjphWE09I7Wx")

# === SUPABASE CONFIGURATION ===
SUPABASE_URL = "https://mqajbtjxwdtwimoavhjz.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xYWpidGp4d2R0d2ltb2F2aGp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgwNDg4NzUsImV4cCI6MjA2MzYyNDg3NX0.JvgIf5-4Xuxef-bQi6JgFHI0CbdpiOouI654cxqwMQo"

# === APP CONFIGURATION ===
APP_NAME = "Proyecto Apollo"
APP_DESCRIPTION = "Chatbot con IA usando OpenAI Assistants"
