# Proyecto Apollo

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Reflex](https://img.shields.io/badge/Reflex-0.8.22-7c3aed.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-Assistants_API-10a37f.svg)
![Supabase](https://img.shields.io/badge/Supabase-Auth_%2B_PostgreSQL-3ecf8e.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Asistente virtual inteligente para ONANO — construido con Reflex y OpenAI Assistants API.**

</div>

---

## Descripción

**Proyecto Apollo** es una aplicación de chat full-stack desarrollada en Python puro con el framework **Reflex**. Actúa como asistente virtual especializado para los distribuidores y clientes de ONANO, respondiendo consultas sobre productos, nanotecnología, plan de compensación y bienestar.

La aplicación integra **OpenAI Assistants API** para conversaciones contextuales e inteligentes, **Supabase Auth** para autenticación segura (vía la librería `suplex`), y **PostgreSQL** (gestionado con SQLModel + Alembic) para la persistencia de conversaciones y usuarios.

---

## Características

- **Autenticación completa**: Registro, inicio de sesión y confirmación de email con Supabase Auth. Incluye toggle de visibilidad en campos de contraseña, validación de fortaleza en tiempo real, y reveal progresivo de campos al detectar `@` en el email.
- **Chat con IA**: Conversaciones contextuales con OpenAI Assistants API, con streaming de respuestas en tiempo real.
- **Gestión de historial**: Creación, edición de título y eliminación de conversaciones. Continuidad de sesión al retomar chats anteriores.
- **Perfil de usuario**: Drawer de perfil con nombre, email y opción de cierre de sesión. Sincronización del nombre post-registro.
- **UI responsive (Mobile First)**: Interfaz adaptada para móvil y escritorio siguiendo el Design System ONANO.
- **Tema claro / oscuro**: Soporte completo de `color_mode` en todos los componentes.
- **Sanitización de respuestas**: Eliminación de artefactos de citación del Assistants API (`fileciteturn`, `【...】`, etc.) antes de mostrarlos al usuario.

---

## Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Framework full-stack | [Reflex](https://reflex.dev) 0.8.22 |
| Lenguaje | Python 3.13 |
| Autenticación | [Suplex](https://github.com/TimChild/suplex) + Supabase Auth |
| Base de datos | PostgreSQL vía Supabase (Connection Pooler) |
| ORM / Migraciones | SQLModel + Alembic |
| IA / LLM | OpenAI Assistants API |
| Design System | ONANO Design System v2.0 (Mobile First) |

---

## Arquitectura del proyecto

```
Proyecto_Apollo/
├── Proyecto_Apollo.py          # Entry point — registro de páginas y app
│
├── components/
│   └── ui/                     # Componentes atómicos reutilizables
│       ├── button.py           # Botón primario / outline / ghost
│       ├── input.py            # Input base + password_input (con toggle ojo)
│       ├── badge.py            # Badges de validación de contraseña
│       ├── toast.py            # Notificaciones toast
│       ├── alert_dialog.py     # Diálogos de confirmación
│       └── user_drawer.py      # Drawer de perfil de usuario
│
├── modules/
│   ├── auth/                   # Módulo de autenticación
│   │   ├── state/
│   │   │   ├── auth_state.py   # AuthState (hereda Suplex): login, registro, toggles
│   │   │   └── confirm_state.py
│   │   └── pages/
│   │       ├── auth_page.py    # Página principal de auth (registro + login)
│   │       └── confirm_page.py # Página de confirmación de email
│   │
│   └── chat/                   # Módulo de chat
│       ├── state/
│       │   └── chat_state.py   # State: conversaciones, mensajes, streaming
│       └── components/
│           ├── chat_components.py     # Mensajes, input de chat
│           ├── sidebar_components.py  # Sidebar desktop + menú de perfil
│           └── header_components.py  # Header móvil + drawer de navegación
│
├── models/
│   └── users.py                # Modelo SQLModel para tabla local 'users'
│
├── styles/
│   ├── colors.py               # Tokens de color del Design System ONANO
│   ├── fonts.py                # Estilos tipográficos (H1, H2, BODY, MICRO)
│   └── common_styles.py        # Estilos compartidos (glassmorphism, etc.)
│
└── config/                     # Configuraciones globales

rxconfig.py                     # Configuración de Reflex + suplex
requirements.txt
alembic/                        # Migraciones de base de datos
```

---

## Instalación y ejecución

### Requisitos previos

- Python 3.13+
- Git
- Cuenta en [OpenAI](https://platform.openai.com) (API Key + Assistant ID)
- Cuenta en [Supabase](https://supabase.com) (proyecto con Auth habilitado)

### 1. Clonar el repositorio

```bash
git clone https://github.com/HyEd-IA/llm-bradrezdev.git
cd llm-bradrezdev
```

### 2. Crear entorno virtual

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# OpenAI
OPENAI_API_KEY=sk-...
API_ASSISTANT_ID=asst_...

# Supabase Auth
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key
SUPABASE_JWT_SECRET=tu-jwt-secret

# Base de datos — usar Connection Pooler (Session mode) para evitar errores IPv6
DATABASE_URL=postgresql://postgres.TU_PROJECT_REF:PASSWORD@aws-0-REGION.pooler.supabase.com:5432/postgres
```

> **Nota sobre la URL de base de datos:** Usar la URL del **Connection Pooler en modo Session** (dominio `pooler.supabase.com`, puerto `5432`) en lugar de la conexión directa (`db.*.supabase.co`). La conexión directa fuerza IPv6, lo cual causa timeouts en entornos locales sin soporte nativo de IPv6.

### 5. Aplicar parche `cookie_secure` (requerido para desarrollo local)

Suplex configura `secure=True` en las cookies por defecto. Los navegadores rechazan cookies `Secure` en `http://localhost`, lo que rompe el flujo de auth. Aplicar el siguiente parche en `.venv/lib/python3.13/site-packages/suplex/suplex.py` y añadir en `rxconfig.py`:

```python
# rxconfig.py
suplex={
    ...
    "cookie_secure": False,  # True en producción
}
```

> Este parche debe re-aplicarse si se recrea el entorno virtual.

### 6. Ejecutar

```bash
reflex run
```

La aplicación estará disponible en `http://localhost:3000`.

---

## Decisiones técnicas y lecciones aprendidas

### `asyncio.to_thread` para llamadas HTTP de Suplex

Las funciones `sign_in_with_password` y `sign_up` de Suplex son síncronas bloqueantes. Llamarlas directamente dentro de un `async def` bloquea el event loop de Reflex, impidiendo que el spinner de carga sea visible antes de la respuesta. Todas las llamadas HTTP se ejecutan con `asyncio.to_thread` y las mutaciones de estado se realizan en el hilo principal, después del `await`.

### `auth_loading` en lugar de `is_loading`

Suplex define `is_loading = False` como atributo de clase plano en la línea 634 de `suplex.py`. Si un substate declara un field con el mismo nombre, el atributo de Suplex gana en la MRO y el `Var` reactivo nunca se genera. El field de loading se llama `auth_loading`.

### `tab_index` como entero

Reflex valida estrictamente los tipos de props. `IconButton.tab_index` espera `int`. Pasar `"-1"` (string) lanza `TypeError` en tiempo de compilación.

### `yield` antes de `rx.redirect()`

Sin un `yield` entre `set_tokens()` y `rx.redirect()`, Reflex batcha ambas operaciones en el mismo delta update. El navegador navega a `/chat` antes de que las cookies sean almacenadas, y `on_load` de la página de chat ve tokens vacíos y redirige de vuelta a `/`.

---

## Licencia

MIT License — Copyright (c) 2025 Bryan Núñez
