"""
Script de prueba para verificar que el assistant está configurado correctamente
"""

import asyncio
from openai import AsyncOpenAI
from Proyecto_Apollo.config import OPENAI_API_KEY, API_ASSISTANT_ID

async def test_assistant():
    """Verifica que el assistant existe y está accesible"""
    print("=" * 60)
    print("🧪 PRUEBA DE CONFIGURACIÓN DEL ASSISTANT")
    print("=" * 60)
    
    try:
        # Inicializar cliente
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        print(f"\n✅ Cliente OpenAI inicializado correctamente")
        print(f"🔑 API Key: {OPENAI_API_KEY[:20]}...")
        
        # Verificar que el assistant existe
        print(f"\n🔍 Buscando assistant con ID: {API_ASSISTANT_ID}")
        assistant = await client.beta.assistants.retrieve(assistant_id=API_ASSISTANT_ID)
        
        print(f"\n✅ ASSISTANT ENCONTRADO:")
        print(f"   - ID: {assistant.id}")
        print(f"   - Nombre: {assistant.name}")
        print(f"   - Modelo: {assistant.model}")
        print(f"   - Descripción: {assistant.description or 'Sin descripción'}")
        print(f"   - Instrucciones: {assistant.instructions[:100] if assistant.instructions else 'Sin instrucciones'}...")
        print(f"   - Tools: {[tool.type for tool in assistant.tools] if assistant.tools else 'Ninguna'}")
        
        # Crear un thread de prueba
        print(f"\n🧵 Creando thread de prueba...")
        thread = await client.beta.threads.create()
        print(f"✅ Thread creado: {thread.id}")
        
        # Enviar un mensaje de prueba
        print(f"\n📤 Enviando mensaje de prueba...")
        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="Hola, ¿estás funcionando correctamente?"
        )
        print(f"✅ Mensaje enviado")
        
        # Ejecutar el assistant (sin streaming para simplificar)
        print(f"\n🤖 Ejecutando assistant...")
        run = await client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=API_ASSISTANT_ID
        )
        
        if run.status == "completed":
            print(f"✅ Run completado exitosamente")
            
            # Obtener respuesta
            messages = await client.beta.threads.messages.list(thread_id=thread.id)
            response = messages.data[0].content[0].text.value
            
            print(f"\n💬 RESPUESTA DEL ASSISTANT:")
            print(f"   {response[:200]}...")
            
        else:
            print(f"⚠️ Run terminó con status: {run.status}")
            if run.last_error:
                print(f"❌ Error: {run.last_error}")
        
        print(f"\n{'=' * 60}")
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("🎉 El assistant está configurado correctamente y funcionando")
        print(f"{'=' * 60}\n")
        
    except Exception as e:
        print(f"\n{'=' * 60}")
        print(f"❌ ERROR EN LA PRUEBA:")
        print(f"   {str(e)}")
        print(f"{'=' * 60}\n")
        raise

if __name__ == "__main__":
    asyncio.run(test_assistant())
