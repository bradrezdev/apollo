# engine.py - VERSIÓN OPTIMIZADA
from sqlmodel import create_engine
from Proyecto_Apollo.config.settings import DATABASE_URL
import threading

# ⭐⭐ CONFIGURACIÓN OPTIMIZADA PARA SUPABASE
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Cambia a True temporalmente para debug
    pool_pre_ping=True,
    pool_size=5,           # Conexiones mantenidas abiertas
    max_overflow=10,       # Máximo adicional bajo carga
    pool_recycle=300,      # Reciclar conexiones cada 5 minutos
    pool_timeout=30,       # Timeout de 30 segundos
    pool_use_lifo=True,    # Mejor para serverless (Supabase)
    connect_args={
        "connect_timeout": 10,  # Timeout de conexión
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 5,
        "keepalives_count": 5,
    }
)

# ⭐⭐ PRECALENTAMIENTO EN SEGUNDO PLANO
def warmup_connection_in_background():
    """Precalienta una conexión en background para evitar cold start"""
    import time
    print("[DEBUG] 🔥 Precalentando conexión a Supabase...")
    start = time.time()
    
    try:
        # Intenta una conexión simple
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        elapsed = time.time() - start
        print(f"[DEBUG] ✅ Conexión precalentada en {elapsed:.2f} segundos")
    except Exception as e:
        print(f"[ERROR] ❌ Error precalentando conexión: {e}")

# Iniciar precalentamiento en thread separado al importar
warmup_thread = threading.Thread(
    target=warmup_connection_in_background,
    daemon=True,
    name="DB-Warmup-Thread"
)
warmup_thread.start()

def get_db_engine():
    """Retorna el motor de base de datos optimizado"""
    return engine