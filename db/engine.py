from sqlmodel import create_engine
from Proyecto_Apollo.config.settings import DATABASE_URL

# Creamos el engine manualmente. 
# pool_pre_ping=True ayuda a recuperar conexiones perdidas.
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

def get_db_engine():
    """Retorna el motor de base de datos para usar en las sesiones"""
    return engine
