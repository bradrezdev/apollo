---
applyTo: '/Users/bradrez/Documents/Proyecto_Apollo'
---

# 🎭 ROL DEL DESARROLLADOR

Toma el rol de un **desarrollador full-stack** con amplio recorrido en la creación de apps móviles. Llevas una carrera profesional con **HTML**, **CSS** y **JavaScript**; sin embargo, desde que comenzaste a trabajar con **Python** te enfocaste más en el desarrollo front-end con **Reflex** (framework de Python). Tienes conocimiento en **PostgreSQL** y siempre desarrollas las bases de datos en **Supabase**. 

El nuevo proyecto que se realizará es un **chatbot con inteligencia artificial** el cuál está conectado con un asistente creado desde **OpenAI**, por lo tanto existe un:
- **`assistantID`**: El ID que conecta específicamente con ese asistente
- **`threadID`**: Me imagino para que lleve un hilo de la conversación y tenga conocimiento previo
- **`runID`**: No tengo idea para qué sería

---

## 📝 MVP DEL CHATBOT

1. **Como usuario** quiero poder enviar un mensaje al chatbot para recibir una respuesta con el conocimiento añadido al asistente dentro de OpenAI.

2. **Como usuario** quiero ver un historial de conversaciones para poder consultar antiguas conversaciones.

3. **Como usuario** quiero enviar un mensaje en alguna conversación antigua para seguir la conversación antigua con el chatbot.

4. **Como usuario** quiero que se le añada un título a la conversación para poder tener idea sobre qué va la conversación.

5. **Como usuario** quiero poder editar el título de la conversación para hacerlo en caso de que sea necesario.

6. **Como usuario** quiero que las conversaciones se vean cronológicamente (de más nuevo a más viejo) para tener en primer lugar de la lista las conversaciones más recientes.

7. **Como usuario** quiero poder iniciar una nueva conversación desde la misma ventana de la conversación actual con el chatbot para mejorar mi experiencia como usuario haciéndolo más práctico.

---

## ⚠️ REGLAS

1. Priorizar el uso de **código limpio** y con el uso de las **mejores prácticas**. Siempre aplicar los principios **KISS**, **DRY**, **YAGNI** y **POO**.

2. Tienes **estrictamente prohibido** crear cualquier nueva feature o implementar algo diferente a lo que se te solicita.

3. Debes de hacer **lo mínimo para resolver**. Debes ser **efectivo** y **eficaz** con el código.

4. Siempre haz una **prueba** para verificar que sí funciona todo.

5. Verifica **paso a paso** las tareas que te solicité y piensa fuerte si estás siguiendo cada tarea **al pie de la letra**.

---

# 🏗️ Arquitectura de Proyecto Apollo

## 📋 Tabla de Contenidos
- [Visión General](#visión-general)
- [Principios de Diseño](#principios-de-diseño)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Guía de Componentes](#guía-de-componentes)
- [Sistema de Estilos](#sistema-de-estilos)
- [Gestión de Estado](#gestión-de-estado)
- [Base de Datos](#base-de-datos)
- [Configuración](#configuración)
- [Flujo de Trabajo](#flujo-de-trabajo)
- [Cómo Agregar Nuevas Features](#cómo-agregar-nuevas-features)

---

## 🎯 Visión General

Proyecto Apollo es un chatbot con IA construido con **Reflex** (Python full-stack framework) que integra la API de OpenAI Assistants. La arquitectura sigue principios de desarrollo limpio y modularidad.

### Stack Tecnológico
- **Framework**: Reflex 0.7.11
- **Base de Datos**: PostgreSQL via Supabase
- **ORM**: SQLModel + Alembic
- **IA**: OpenAI Assistants API
- **Lenguaje**: Python 3.13

---

## 🎨 Principios de Diseño

Esta arquitectura se basa en 4 principios fundamentales:

### 1. **KISS** (Keep It Simple, Stupid)
- Cada componente hace UNA cosa bien
- Evitamos complejidad innecesaria
- Código claro y directo

### 2. **DRY** (Don't Repeat Yourself)
- Estilos centralizados en archivos reutilizables
- Componentes modulares que se pueden importar
- Configuración única en un solo lugar

### 3. **YAGNI** (You Aren't Gonna Need It)
- Solo implementamos lo necesario para el MVP
- No agregamos funcionalidades "por si acaso"
- Cada línea de código tiene un propósito claro

### 4. **POO** (Programación Orientada a Objetos)
- Herencia de estados: `State → DBState → rx.State`
- Encapsulación de lógica de negocio
- Separación de responsabilidades

---

## 📁 Estructura del Proyecto

```
Proyecto_Apollo/
├── Proyecto_Apollo.py          # 🚪 Punto de entrada principal
├── state.py                    # 🧠 Lógica de chat y UI
├── supabase_client.py          # 🔌 Cliente de Supabase
│
├── components/                 # 🧩 Componentes UI modulares
│   ├── __init__.py
│   ├── chat/                   # 💬 Componentes de chat
│   │   ├── __init__.py
│   │   └── chat_components.py
│   ├── sidebar/                # 📋 Sidebar con historial
│   │   ├── __init__.py
│   │   └── sidebar_components.py
│   ├── header/                 # 🎯 Headers y navegación
│   │   ├── __init__.py
│   │   └── header_components.py
│   └── layout/                 # 🏗️ Componentes de layout
│       ├── __init__.py
│       └── banner.py
│
├── styles/                     # 🎨 Sistema de estilos
│   ├── __init__.py
│   ├── colors.py               # 🌈 Paleta de colores
│   ├── chat_styles.py          # Estilos de chat
│   ├── sidebar_styles.py       # Estilos de sidebar
│   ├── header_styles.py        # Estilos de header
│   └── layout_styles.py        # Estilos de layout
│
├── config/                     # ⚙️ Configuración centralizada
│   ├── __init__.py
│   └── settings.py             # API keys y constantes
│
└── db/                         # 🗄️ Capa de datos
    ├── conversations.py        # Modelo de BD
    └── db_state.py             # Operaciones de BD

alembic/                        # 🔄 Migraciones de BD
├── versions/
└── env.py
```

---

## 🧩 Guía de Componentes

### Anatomía de un Componente

Cada componente sigue esta estructura:

```python
# Proyecto_Apollo/components/chat/chat_components.py

import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo.styles.chat_styles import (
    chat_container_style,
    message_style
)

def mi_componente() -> rx.Component:
    """
    Descripción clara del propósito del componente
    
    Returns:
        rx.Component: Componente de Reflex renderizable
    """
    return rx.box(
        # ... estructura del componente
        **chat_container_style  # Aplicar estilos
    )
```

### Organización por Categorías

#### 📂 `components/chat/`
**Propósito**: Todo lo relacionado con mensajes y entrada de usuario

**Componentes**:
- `chat_message()`: Muestra pregunta y respuesta
- `chat_container_desktop()`: Container con scroll para desktop
- `chat_container_mobile()`: Container optimizado para móvil
- `desktop_chat_input()`: Input de texto para desktop
- `mobile_chat_input()`: Input de texto para móvil

**Cuándo crear aquí**: Cualquier componente que maneje la visualización o entrada de mensajes.

#### 📂 `components/sidebar/`
**Propósito**: Navegación y lista de conversaciones

**Componentes**:
- `desktop_sidebar()`: Sidebar fijo para desktop
- `conversation_list_item()`: Item individual de conversación
- `new_conversation_button()`: Botón para nueva conversación

**Cuándo crear aquí**: Componentes relacionados con navegación e historial.

#### 📂 `components/header/`
**Propósito**: Headers y navegación móvil

**Componentes**:
- `desktop_header()`: Header simple para desktop
- `mobile_header()`: Header con drawer para móvil
- `mobile_drawer_sidebar()`: Contenido del drawer móvil

**Cuándo crear aquí**: Componentes de encabezado o navegación superior.

#### 📂 `components/layout/`
**Propósito**: Componentes estructurales y banners

**Componentes**:
- `desktop_banner()`: Banner de bienvenida

**Cuándo crear aquí**: Componentes que estructuran el layout general.

---

## 🎨 Sistema de Estilos

### Filosofía de Estilos

Los estilos están **completamente separados** de los componentes:

```python
# ❌ MAL - Estilos inline
rx.box(
    "Contenido",
    background_color="#1a1a1a",
    padding="20px",
    border_radius="8px"
)

# ✅ BIEN - Estilos importados
from Proyecto_Apollo.styles.chat_styles import container_style

rx.box(
    "Contenido",
    **container_style
)
```

### Paleta de Colores

Los colores están centralizados en `styles/colors.py`:

```python
from Proyecto_Apollo.styles.colors import (
    PRIMARY_BG,      # Fondo principal
    SECONDARY_BG,    # Fondo secundario
    TEXT_PRIMARY,    # Texto principal
    ACCENT_COLOR,    # Color de acento
)
```

### Crear Nuevos Estilos

1. **Identifica la categoría**: ¿Es para chat, sidebar, header o layout?
2. **Abre el archivo correspondiente**: `styles/{categoria}_styles.py`
3. **Define el estilo como diccionario**:

```python
# styles/chat_styles.py

mi_nuevo_estilo = {
    "background_color": PRIMARY_BG,
    "padding": "1rem",
    "border_radius": "8px",
    "box_shadow": "0 2px 4px rgba(0,0,0,0.1)",
}
```

4. **Exporta en `__init__.py`**:

```python
# styles/__init__.py
from .chat_styles import mi_nuevo_estilo
```

5. **Usa en tu componente**:

```python
from Proyecto_Apollo.styles import mi_nuevo_estilo

def mi_componente():
    return rx.box("Contenido", **mi_nuevo_estilo)
```

---

## 🧠 Gestión de Estado

### Jerarquía de Estados

```
rx.State (Reflex base)
    ↑
DBState (db/db_state.py) - Operaciones de base de datos
    ↑
State (state.py) - Lógica de chat y UI
```

### DBState - Capa de Datos

**Ubicación**: `db/db_state.py`

**Responsabilidad**: Todas las operaciones con la base de datos

**Métodos clave**:
```python
class DBState(rx.State):
    conversations: list[dict] = []
    
    def load_conversations(self):
        """Carga todas las conversaciones"""
    
    def create_new_conversation(self, thread_id: str):
        """Crea una nueva conversación"""
    
    def update_conversation_title(self, conversation_id: int, new_title: str):
        """Actualiza el título de una conversación"""
    
    def get_conversation_by_thread(self, thread_id: str):
        """Obtiene conversación por thread_id"""
```

### State - Capa de Lógica

**Ubicación**: `Proyecto_Apollo/state.py`

**Responsabilidad**: Lógica de chat, streaming de OpenAI, manejo de UI

**Hereda de**: `DBState`

**Propiedades clave**:
```python
class State(DBState):
    chat_history: list[tuple[str, str]] = []
    question: str = ""
    is_loading: bool = False
    current_thread_id: str = ""
    is_drawer_open: bool = False
```

**Métodos clave**:
```python
async def answer(self):
    """Envía pregunta a OpenAI y recibe respuesta en streaming"""

def load_conversation_and_messages(self, thread_id: str):
    """Carga una conversación específica y sus mensajes"""

def on_load(self):
    """Se ejecuta al cargar la aplicación"""
```

### Cuándo Agregar al State

- **Datos temporales de UI**: Agregar a `State`
- **Datos que necesitan persistirse**: Agregar a `DBState`
- **Computed vars** (propiedades calculadas): Usar `@rx.var`

```python
class State(DBState):
    question: str = ""
    
    @rx.var
    def has_messages(self) -> bool:
        """Computed var - se actualiza automáticamente"""
        return len(self.chat_history) > 0
```

---

## 🗄️ Base de Datos

### Modelo de Datos

**Ubicación**: `db/conversations.py`

```python
class Conversations(rx.Model, table=True):
    id: int | None = Field(default=None, primary_key=True)
    thread_id: str = Field(unique=True, index=True)
    title: str = Field(default="Nueva conversación")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

### Migraciones con Alembic

Reflex usa Alembic automáticamente:

```bash
# Crear migración después de cambiar el modelo
reflex db makemigrations --message "descripción del cambio"

# Aplicar migraciones
reflex db migrate
```

### Agregar un Nuevo Modelo

1. **Crea el modelo** en `db/`:

```python
# db/users.py
import reflex as rx
from sqlmodel import Field
from datetime import datetime

class Users(rx.Model, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
```

2. **Crea las operaciones** en `db/db_state.py`:

```python
def create_user(self, email: str):
    with rx.session() as session:
        user = Users(email=email)
        session.add(user)
        session.commit()
```

3. **Genera y aplica migración**:

```bash
reflex db makemigrations --message "add users table"
reflex db migrate
```

---

## ⚙️ Configuración

### Archivo Central

**Ubicación**: `config/settings.py`

Todas las API keys y constantes están centralizadas:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_ASSISTANT_ID = os.getenv("API_ASSISTANT_ID")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# App
APP_NAME = "Apollo"
APP_DESCRIPTION = "Chatbot con IA"
```

### Agregar Nueva Configuración

1. **Añadir al `.env`**:
```
NEW_API_KEY=tu_clave_aqui
```

2. **Importar en `settings.py`**:
```python
NEW_API_KEY = os.getenv("NEW_API_KEY")
```

3. **Usar en tu código**:
```python
from Proyecto_Apollo.config.settings import NEW_API_KEY
```

---

## 🔄 Flujo de Trabajo

### Flujo de Mensaje de Usuario

```
1. Usuario escribe mensaje
   ↓
2. desktop_chat_input() captura el texto
   ↓
3. State.set_question() actualiza el estado
   ↓
4. State.answer() se ejecuta on_submit
   ↓
5. OpenAI procesa con streaming
   ↓
6. Respuesta se agrega a chat_history
   ↓
7. chat_container muestra el nuevo mensaje
```

### Flujo de Carga de Conversación

```
1. Usuario hace clic en conversación del sidebar
   ↓
2. conversation_list_item() llama a State.load_conversation_and_messages()
   ↓
3. DBState.get_conversation_by_thread() consulta la BD
   ↓
4. OpenAI API obtiene mensajes del thread
   ↓
5. State actualiza chat_history
   ↓
6. UI se re-renderiza con mensajes cargados
```

---

## 🚀 Cómo Agregar Nuevas Features

### Ejemplo: Agregar "Eliminar Conversación"

#### Paso 1: Modelo de Datos (si es necesario)
```python
# Ya existe en db/conversations.py, no se requiere cambio
```

#### Paso 2: Lógica de Base de Datos

```python
# db/db_state.py

def delete_conversation(self, conversation_id: int):
    """Elimina una conversación por su ID"""
    with rx.session() as session:
        conversation = session.get(Conversations, conversation_id)
        if conversation:
            session.delete(conversation)
            session.commit()
            # Recargar lista
            self.load_conversations()
```

#### Paso 3: Componente UI

```python
# components/sidebar/sidebar_components.py

def delete_button(conversation_id: int) -> rx.Component:
    """Botón para eliminar conversación"""
    return rx.button(
        rx.icon("trash-2", size=16),
        on_click=State.delete_conversation(conversation_id),
        color_scheme="red",
        variant="ghost",
        size="1",
    )
```

#### Paso 4: Integrar en Componente Existente

```python
# components/sidebar/sidebar_components.py

def conversation_list_item(conversation: dict) -> rx.Component:
    return rx.hstack(
        rx.button(
            conversation["title"],
            on_click=State.load_conversation_and_messages(conversation["thread_id"]),
        ),
        delete_button(conversation["id"]),  # ← Agregar aquí
    )
```

#### Paso 5: Estilos (si es necesario)

```python
# styles/sidebar_styles.py

delete_button_style = {
    "color": "red.500",
    "hover": {"background_color": "red.100"},
}
```

#### Paso 6: Probar

```bash
reflex run
```

---

## 📝 Checklist para Nuevas Features

Antes de considerar una feature completa:

- [ ] ✅ Modelo de datos actualizado (si aplica)
- [ ] ✅ Migración de BD ejecutada (si aplica)
- [ ] ✅ Lógica agregada en `DBState` o `State`
- [ ] ✅ Componente UI creado en carpeta correcta
- [ ] ✅ Estilos definidos en archivo correspondiente
- [ ] ✅ Exports actualizados en `__init__.py`
- [ ] ✅ Componente integrado en layout
- [ ] ✅ Probado en desktop Y móvil
- [ ] ✅ Código sigue principios KISS, DRY, YAGNI

---

## 🔧 Comandos Útiles

```bash
# Iniciar aplicación
reflex run

# Modo desarrollo (hot reload)
reflex run --env dev

# Crear migración
reflex db makemigrations --message "descripción"

# Aplicar migraciones
reflex db migrate

# Limpiar y rebuildar
reflex clean && reflex init && reflex run
```

---

## 🎓 Recursos

- [Documentación de Reflex](https://reflex.dev/docs)
- [OpenAI Assistants API](https://platform.openai.com/docs/assistants)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [Supabase Docs](https://supabase.com/docs)

---

## 👥 Para Nuevos Desarrolladores

### Primeros Pasos

1. **Lee este documento completo** - Entiende la arquitectura antes de tocar código
2. **Explora `components/`** - Familiarízate con los componentes existentes
3. **Revisa `state.py`** - Comprende cómo fluyen los datos
4. **Prueba localmente** - Ejecuta `reflex run` y juega con la app

### Reglas de Oro

1. **Un archivo, un propósito** - Si un archivo hace múltiples cosas, divídelo
2. **Estilos separados** - NUNCA pongas estilos inline, usa archivos de estilos
3. **No reinventes la rueda** - Si existe un componente similar, reutilízalo
4. **Pregunta antes de cambiar** - La arquitectura tiene un propósito, respétalo
5. **Prueba en móvil Y desktop** - Cada cambio debe funcionar en ambos

---

# 🚀 Proyecto Apollo - README

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Reflex](https://img.shields.io/badge/Reflex-0.7.11-purple.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-Assistants-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-orange.svg)

Un chatbot inteligente construido con Reflex y OpenAI Assistants API, con arquitectura modular y clean code.

</div>

---

## ✨ Características

### MVP Actual

- ✅ **Chat con IA**: Envía mensajes y recibe respuestas en tiempo real usando OpenAI Assistants
- ✅ **Historial de Conversaciones**: Visualiza todas tus conversaciones anteriores
- ✅ **Continuación de Conversaciones**: Retoma conversaciones antiguas donde las dejaste
- ✅ **Títulos Editables**: Cada conversación tiene un título que puedes personalizar
- ✅ **Orden Cronológico**: Las conversaciones más recientes aparecen primero
- ✅ **Nueva Conversación Rápida**: Inicia un nuevo chat desde cualquier lugar
- ✅ **Responsive Design**: Funciona perfectamente en desktop y móvil

### Características Técnicas

- 🏗️ **Arquitectura Modular**: Componentes separados y reutilizables
- 🎨 **Sistema de Estilos Centralizado**: Estilos organizados por categoría
- 🗄️ **Base de Datos PostgreSQL**: Persistencia de conversaciones en Supabase
- 🔄 **Migraciones Automáticas**: Alembic integrado con Reflex
- 🧠 **Estado Jerárquico**: DBState → State → rx.State
- 📱 **Mobile-First**: Diseño optimizado para todos los dispositivos

---

## 🛠️ Instalación

### Prerrequisitos

- Python 3.13+
- PostgreSQL (o cuenta en Supabase)
- Cuenta en OpenAI con API key

### Pasos

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/Proyecto_Apollo.git
cd Proyecto_Apollo
```

2. **Crear y activar entorno virtual**

```bash
python -m venv apollo
source apollo/bin/activate  # En Windows: apollo\Scripts\activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

Crea un archivo `.env` en la raíz del proyecto:

```env
# OpenAI
OPENAI_API_KEY=sk-tu-api-key-aqui
API_ASSISTANT_ID=asst_tu-assistant-id

# Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-supabase-key

# Database
DATABASE_URL=postgresql://usuario:password@host:5432/database
```

5. **Ejecutar migraciones**

```bash
reflex db migrate
```

6. **Iniciar la aplicación**

```bash
reflex run
```

La aplicación estará disponible en `http://localhost:3000`

---

## 🎮 Uso

### Interfaz Desktop

1. **Sidebar Izquierdo**: Muestra todas tus conversaciones
2. **Área Central**: Chat activo con mensajes
3. **Input Inferior**: Escribe tu mensaje y presiona Enter

### Interfaz Móvil

1. **Menú Hamburguesa**: Accede al historial de conversaciones
2. **Chat**: Área principal optimizada para táctil
3. **Input Fijo**: Siempre accesible en la parte inferior

### Acciones Rápidas

- **Nueva Conversación**: Clic en "Nueva conversación" en el header
- **Cargar Conversación**: Clic en cualquier conversación del historial
- **Editar Título**: Clic en el ícono de edición junto al título (próximamente)

---

## 👨‍💻 Desarrollo

### Scripts Útiles

```bash
# Desarrollo con hot reload
reflex run --env dev

# Limpiar cache
reflex clean

# Crear migración
reflex db makemigrations --message "descripción"

# Aplicar migraciones
reflex db migrate

# Verificar sintaxis de Python
python -m py_compile archivo.py
```

### Reglas de Contribución

- ✅ Un archivo, un propósito
- ✅ Estilos siempre en archivos separados
- ✅ Nombres descriptivos en español
- ✅ Docstrings en todas las funciones
- ✅ Probar en múltiples dispositivos
- ❌ No estilos inline
- ❌ No código duplicado
- ❌ No features innecesarias

---

## 🗺️ Roadmap

### Fase 1: MVP ✅ (Completado)

- [x] Enviar mensajes al chatbot
- [x] Ver historial de conversaciones
- [x] Continuar conversaciones antiguas
- [x] Títulos de conversaciones
- [x] Editar títulos
- [x] Orden cronológico
- [x] Nueva conversación desde anywhere

### Fase 2: Mejoras de UX (En Progreso)

- [ ] Edición de títulos desde UI
- [ ] Eliminación de conversaciones
- [ ] Búsqueda en historial
- [ ] Etiquetas/categorías
- [ ] Modo oscuro

### Fase 3: Autenticación

- [ ] Sistema de login
- [ ] Registro de usuarios
- [ ] Gestión de sesiones
- [ ] Perfiles de usuario

### Fase 4: Features Avanzadas

- [ ] Compartir conversaciones
- [ ] Exportar chat a PDF/MD
- [ ] Comandos slash (/)
- [ ] Shortcuts de teclado
- [ ] Respuestas sugeridas

---

**Última actualización**: 11 de diciembre de 2025  
**Versión de Reflex**: 0.7.11  
**Arquitectura**: Modular basada en separación de responsabilidades
