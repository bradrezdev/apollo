"""Script de prueba para verificar la conexión con la base de datos"""

from db.conversations import Conversations
from sqlmodel import Session, select
from reflex.model import Model

def test_connection():
    """Prueba la conexión con la base de datos usando SQLModel"""
    try:
        # Obtener el engine de Reflex
        engine = Model.get_db_engine()
        
        # Crear una sesión
        with Session(engine) as session:
            # Intentar consultar conversaciones
            statement = select(Conversations)
            results = session.exec(statement).all()
            
            print("✅ Conexión exitosa con la base de datos PostgreSQL")
            print(f"✅ Tabla 'conversations' existe y es accesible")
            print(f"📊 Conversaciones encontradas: {len(results)}")
            
            if results:
                print("\n📝 Conversaciones:")
                for conv in results:
                    print(f"   - {conv.title} (ID: {conv.id}, Thread: {conv.thread_id})")
            
            return True
            
    except Exception as e:
        print("❌ Error al conectar con la base de datos:")
        print(f"   {str(e)}")
        print("\n💡 Asegúrate de haber ejecutado 'reflex db migrate'")
        return False

if __name__ == "__main__":
    test_connection()
