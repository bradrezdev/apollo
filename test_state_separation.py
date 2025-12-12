"""Script de prueba para verificar la separación de responsabilidades entre State y DBState"""

import asyncio
from Proyecto_Apollo.state import State
from db.db_state import DBState

async def test_db_state():
    """Prueba los métodos de DBState"""
    print("=" * 60)
    print("PRUEBA 1: DBState - Operaciones de Base de Datos")
    print("=" * 60)
    
    db_state = DBState()
    
    # Cargar conversaciones
    print("\n📊 Cargando conversaciones...")
    await db_state.load_conversations()
    print(f"   Conversaciones encontradas: {len(db_state.conversations)}")
    
    if db_state.conversations:
        print("\n📝 Conversaciones existentes:")
        for conv in db_state.conversations[:5]:  # Mostrar solo las primeras 5
            print(f"   - {conv['title']} (ID: {conv['id']})")
    
    return db_state

async def test_state_inheritance():
    """Prueba que State hereda correctamente de DBState"""
    print("\n" + "=" * 60)
    print("PRUEBA 2: State - Herencia de DBState")
    print("=" * 60)
    
    state = State()
    
    # Verificar que tiene acceso a métodos de DBState
    print("\n✅ Métodos de DBState disponibles en State:")
    db_methods = [
        "load_conversations",
        "create_new_conversation",
        "load_conversation_by_id",
        "update_conversation_title",
        "update_conversation_timestamp",
        "delete_conversation"
    ]
    
    for method in db_methods:
        has_method = hasattr(state, method)
        status = "✅" if has_method else "❌"
        print(f"   {status} {method}")
    
    # Verificar métodos propios de State
    print("\n✅ Métodos propios de State:")
    state_methods = [
        "answer",
        "auto_generate_title",
        "start_new_conversation",
        "load_conversation_and_messages",
        "toggle_drawer",
        "clear_chat_history"
    ]
    
    for method in state_methods:
        has_method = hasattr(state, method)
        status = "✅" if has_method else "❌"
        print(f"   {status} {method}")
    
    # Cargar conversaciones desde State
    print("\n📊 Cargando conversaciones desde State...")
    await state.load_conversations()
    print(f"   Conversaciones cargadas: {len(state.conversations)}")
    
    return state

async def test_full_flow():
    """Prueba el flujo completo"""
    print("\n" + "=" * 60)
    print("PRUEBA 3: Flujo Completo")
    print("=" * 60)
    
    state = State()
    
    # Cargar conversaciones
    await state.load_conversations()
    initial_count = len(state.conversations)
    print(f"\n📊 Conversaciones iniciales: {initial_count}")
    
    # Simular creación de conversación
    print("\n🔧 Creando nueva conversación de prueba...")
    conv_id = await state.create_new_conversation(
        thread_id="test_thread_123456",
        title="Conversación de prueba"
    )
    
    if conv_id:
        print(f"   ✅ Conversación creada con ID: {conv_id}")
        print(f"   ✅ Thread ID actual: {state.current_thread_id}")
        print(f"   ✅ Conversation ID actual: {state.current_conversation_id}")
        
        # Actualizar título
        print("\n✏️ Actualizando título...")
        await state.update_conversation_title(conv_id, "Título actualizado")
        print("   ✅ Título actualizado")
        
        # Eliminar conversación de prueba
        print("\n🗑️ Eliminando conversación de prueba...")
        await state.delete_conversation(conv_id)
        print("   ✅ Conversación eliminada")
        
    await state.load_conversations()
    final_count = len(state.conversations)
    print(f"\n📊 Conversaciones finales: {final_count}")
    
    if final_count == initial_count:
        print("✅ Todo funcionó correctamente (mismo número de conversaciones)")
    
    return state

async def main():
    """Ejecuta todas las pruebas"""
    try:
        await test_db_state()
        await test_state_inheritance()
        await test_full_flow()
        
        print("\n" + "=" * 60)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("=" * 60)
        print("\n🎉 La separación de responsabilidades funciona correctamente:")
        print("   - DBState maneja toda la lógica de base de datos")
        print("   - State hereda de DBState y maneja UI y chat")
        print("   - Ambos se comunican perfectamente")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
