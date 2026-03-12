🧠 Project Manager - Cerebro de ATLAS
Plan de Acción: Integración de Suplex + reflex db en Apollo
Después de analizar a fondo el código fuente de Suplex v0.2.7, el estado actual de Apollo, la documentación de Reflex sobre DB/migrations/client-storage, y consultar los perfiles de Jazmin (Backend) y Adrian (Full-Stack), presento el plan coordinado.
---
Diagnóstico del Estado Actual
| Aspecto | Estado | Problemas Detectados |
|---------|--------|---------------------|
| Auth (Supabase SDK) | Parcial | Tokens no se persisten, sign_up nunca se llama, no hay auth guards |
| DB Models | Inconsistente | Modelos usan question_encrypted pero DBState referencia question/answer |
| Alembic | Roto | env.py tiene target_metadata = None, alembic.ini tiene URL placeholder |
| State Hierarchy | Desconectada | AuthState y DBState no comparten datos. Chat no sabe quién es el usuario |
| User Scoping | Inexistente | Conversations se cargan sin filtro WHERE user_id = ? |
---
## Qué es Suplex y Por Qué Resuelve Todo Esto
Suplex (pip install suplex) es una librería que extiende rx.State y proporciona:
1. Suplex(rx.State) - Un State base que maneja automáticamente:
   - access_token y refresh_token como rx.Cookie (persistencia en browser)
   - Decodificación automática de JWT con computed vars (user_id, user_email, user_is_authenticated, user_token_expired, etc.)
   - Refresh automático de sesión cuando el token expira
   - Métodos completos: sign_up(), sign_in_with_password(), sign_in_with_oauth(), log_out(), get_user(), update_user(), refresh_session(), reset_password_email()
2. Query(rx.Base) - Un query builder que usa la REST API de Supabase (PostgREST) con:
   - Filtros encadenables: .eq(), .gt(), .like(), .in_(), etc.
   - Operaciones CRUD: .select(), .insert(), .update(), .delete(), .upsert()
   - Soporte para .admin() (bypass RLS con service_role)
   - Ejecución sync y async
3. Configuración via rxconfig.py usando config.suplex = {...} 
---

# Plan de Acción en 5 Fases
---
## FASE 1: Instalación y Configuración Base
Agente responsable: Adrian (Full-Stack) con supervisión de Jazmin (Backend)
| # | Tarea | Detalle |
|---|-------|---------|
| 1.1 | Instalar Suplex | pip install suplex + actualizar requirements.txt |
| 1.2 | Configurar rxconfig.py | Agregar bloque suplex={...} con api_url, api_key, jwt_secret (opcional, las nuevas versiones de Supabase usan JWKS automático), cookie_max_age, debug |
| 1.3 | Actualizar .env | Agregar SUPABASE_JWT_SECRET (si se usa API legacy) y SUPABASE_SERVICE_ROLE_KEY (para queries admin) |
| 1.4 | Limpiar supabase_client.py | Ya no se necesita el singleton de create_client() porque Suplex hace las llamadas HTTP directamente |
Ejemplo de rxconfig.py resultante:
import reflex as rx
from Proyecto_Apollo.config.settings import (
    APP_NAME, DATABASE_URL, SUPABASE_URL, SUPABASE_ANON_KEY
)
config = rx.Config(
    app_name=APP_NAME,
    db_url=DATABASE_URL,
    suplex={
        "api_url": SUPABASE_URL,
        "api_key": SUPABASE_ANON_KEY,
        # "jwt_secret": SUPABASE_JWT_SECRET,  # Solo si API legacy
        # "service_role": SUPABASE_SERVICE_ROLE_KEY,  # Para queries admin
        "cookie_max_age": 60 * 60 * 24 * 7,  # 7 días
        "debug": True,  # Desactivar en producción
    },
)
---

## FASE 2: Migración de Modelos a rx.Model + reflex db init
Agente responsable: Jazmin (Backend Architect)
Esta fase resuelve el caos actual de Alembic y los modelos inconsistentes.
| # | Tarea | Detalle |
|---|-------|---------|
| 2.1 | Eliminar directorio alembic/ actual | Las migraciones actuales están rotas (target_metadata = None) |
| 2.2 | Eliminar alembic.ini | Se regenerará con reflex db init |
| 2.3 | Convertir modelos de SQLModel a rx.Model | Los modelos actuales en db/ usan SQLModel directamente. Deben heredar de rx.Model para que Reflex los detecte automáticamente |
| 2.4 | Mover modelos a Proyecto_Apollo/models/ | Dentro del paquete de la app para que reflex db makemigrations los detecte |
| 2.5 | Ejecutar reflex db init | Inicializa Alembic correctamente con metadata del proyecto |
| 2.6 | Ejecutar reflex db makemigrations --message 'initial schema' | Genera la migración inicial |
| 2.7 | Ejecutar reflex db migrate | Aplica la migración |
Decision importante -- dos caminos para las queries de datos:
| Opción | Cómo funciona | Ventaja | Desventaja |
|--------|---------------|---------|------------|
| A) rx.Model + rx.session() | Los modelos se definen como archivos Python con rx.Model. Las queries usan rx.session() (SQLAlchemy) | Control total, queries complejas, joins nativos | Más código manual |
| B) Suplex Query (PostgREST) | Las tablas se crean via reflex db pero las queries van por la REST API de Supabase | Sintaxis fluida, respeta RLS automáticamente | No soporta joins complejos, depende de la red |
| C) Híbrido | Modelos con rx.Model, queries simples con Suplex Query, queries complejas con rx.session() | Lo mejor de ambos mundos | Dos patrones de acceso a datos |
---

## FASE 3: Reestructurar el Sistema de Autenticación con Suplex
Agente responsable: Adrian (Full-Stack) con revisión de Jazmin
| # | Tarea | Detalle |
|---|-------|---------|
| 3.1 | Crear AuthState(Suplex) | El nuevo AuthState hereda de Suplex en vez de rx.State. Esto le da automáticamente: cookies de tokens, computed vars de usuario, métodos de auth |
| 3.2 | Reestructurar herencia de States | La cadena debe ser: Suplex -> AuthState -> DBState -> ChatState para que TODOS los estados tengan acceso al user_id y access_token |
| 3.3 | Implementar sign_up real | Conectar el flujo de registro UI al self.sign_up(email, password, options={"data": {...}}) de Suplex |
| 3.4 | Implementar sign_in real | Conectar el login UI al self.sign_in_with_password(email, password) de Suplex. Los tokens se guardan automáticamente en cookies |
| 3.5 | Implementar log_out | Agregar botón de logout que llame a self.log_out() |
| 3.6 | Persistencia de sesión | Suplex usa rx.Cookie para access_token y refresh_token. Al recargar la página, los tokens persisten. El on_load de cada página debe verificar self.user_is_authenticated |
| 3.7 | Auth guards en rutas | Agregar verificación en on_load de /chat: si not self.user_is_authenticated -> rx.redirect("/") |
| 3.8 | Refresh automático | Suplex ya maneja esto: si user_token_expired y let_jwt_expire=False, llama a refresh_session() automáticamente antes de cada query |
Ejemplo de la nueva herencia:
from suplex import Suplex
class AuthState(Suplex):
    """Auth state que hereda de Suplex."""
    step: int = 1
    # ... campos del flujo UI
    
    def submit_login(self):
        result = self.sign_in_with_password(email=self.email, password=self.password)
        # Tokens guardados automáticamente en cookies
        # self.user_id, self.user_email ya disponibles via computed vars
        return rx.redirect("/chat")
class DBState(AuthState):
    """DB operations - ahora tiene acceso a user_id via Suplex."""
    
    def load_conversations_async(self):
        # Ahora puede filtrar por usuario:
        # WHERE user_id = self.user_id
        pass
class ChatState(DBState):
    """Chat state - hereda auth + DB."""
    pass
---

## FASE 4: Conectar Auth con Datos (User Scoping)
Agente responsable: Jazmin (Backend) + Adrian (implementación)
| # | Tarea | Detalle |
|---|-------|---------|
| 4.1 | Filtrar conversations por user_id | Modificar load_conversations_async() para usar WHERE user_id = self.user_id |
| 4.2 | Asignar user_id al crear conversations | Cuando se crea una nueva conversación, setear user_id con el ID del usuario autenticado (desde Suplex self.user_id) |
| 4.3 | Sincronizar usuario Supabase Auth con tabla users | Al hacer signup/login, crear o buscar el registro en la tabla users local |
| 4.4 | Eliminar hardcoded user data | Quitar user_name: str = "Bryan Nunez" y user_email: str = "b.nunez@hotmail.es" del ChatState. Ahora vienen de self.user_email y self.user_metadata |
| 4.5 | Fix column mismatch | Alinear DBState para que use question_encrypted/answer_encrypted o revertir a question/answer via nueva migración |
---
FASE 5: Limpieza, Testing y Documentación
Agente responsable: Adrian (limpieza) + Giovann (QA) + Project Manager (docs)
| # | Tarea | Detalle |
|---|-------|---------|
| 5.1 | Eliminar db/engine.py | Ya no se necesita el engine custom. rxconfig.py con db_url maneja la conexión. Suplex usa HTTP para queries PostgREST |
| 5.2 | Eliminar archivos de test de DB | test_db.py, test_direct.py, test_pooler.py, test_regions.py ya no aplican |
| 5.3 | Eliminar dependencia de supabase SDK | Si todas las queries van por Suplex Query o rx.session(), ya no se necesita supabase Python SDK |
| 5.4 | Testing de flujo completo | Signup -> Login -> Persistencia (refresh page) -> Chat con user scoping -> Logout |
| 5.5 | Actualizar documentación ATLAS | Actualizar docs/projects/apollo.md y patterns/autenticacion.md con los nuevos patrones de Suplex |
---
Estructura de Archivos Resultante
apollo/
├── rxconfig.py                    # + bloque suplex={...}
├── Proyecto_Apollo/
│   ├── models/                    # NUEVO - Modelos rx.Model
│   │   ├── __init__.py
│   │   ├── user.py                # rx.Model (users table)
│   │   ├── conversation.py        # rx.Model (conversations table)
│   │   └── message.py             # rx.Model (messages table)
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── state/
│   │   │   │   └── auth_state.py  # AuthState(Suplex) - hereda de Suplex
│   │   │   └── pages/
│   │   │       └── auth_page.py   # UI del flujo auth (6 steps)
│   │   └── chat/
│   │       ├── state/
│   │       │   ├── db_state.py    # DBState(AuthState) 
│   │       │   └── chat_state.py  # ChatState(DBState)
│   │       └── ...
│   └── ...
├── alembic/                       # Generado por 'reflex db init'
│   ├── env.py                     # Correctamente configurado por Reflex
│   └── versions/                  # Migraciones limpias
└── alembic.ini                    # Generado por 'reflex db init'

### To summ

Goal
The user (Bryan) is working on Project Apollo, an AI chatbot application built with Reflex (Python), Supabase (PostgreSQL + Auth), and OpenAI Assistants API. The overarching goals in this conversation were:
1. Fix a toast component error — The show_toast event handler was returning a visual component (rx.Box) instead of an event (rx.EventSpec), causing a Reflex backend exception.
2. Create a customizable toast system — Build a wrapper around rx.toast that supports .success(), .error(), .warning(), .info() methods with configurable description, bg_color, color, and close_button parameters.
3. Develop a comprehensive plan for integrating Suplex (a Python library for Supabase auth in Reflex) + reflex db init for database migrations management.
Instructions
- The user renamed component files to remove the "atoms" prefix — components should be named by what they are (e.g., button.py, toast.py).
- The user wants the toast system to be a class-based wrapper (CustomToastWrapper) that delegates to rx.toast native events, NOT visual components.
- The user explicitly prefers the Project Manager agent (@project-manager) to coordinate work and invoke other agents as needed.
- All agents must start responses with their signature emoji/badge.
- For the Suplex + DB plan, the user answered three key architecture questions:
  - Queries approach: A) Solo rx.session() with SQLAlchemy (recommended) — NOT Suplex Query PostgREST
  - Existing tables: Fresh start — delete and recreate tables via reflex db (data is test data)
  - Engine: Use db_url standard in rxconfig — drop the custom engine.py with connection pooling
Discoveries
About Suplex (v0.2.7)
- Suplex is a real PyPI package (pip install suplex) — source code was fully extracted and analyzed from the wheel
- It provides a Suplex(rx.State) class that automatically manages:
  - access_token and refresh_token as rx.Cookie (browser persistence)
  - JWT decoding with computed vars: user_id, user_email, user_is_authenticated, user_token_expired, claims, user_metadata, app_metadata, etc.
  - Auto-refresh of sessions when token expires (if let_jwt_expire=False)
  - Methods: sign_up(), sign_in_with_password(), sign_in_with_oauth(), log_out(), get_user(), update_user(), refresh_session(), reset_password_email(), exchange_code_for_session()
- It also provides a Query(rx.Base) class for Supabase PostgREST queries (but user chose NOT to use this — using rx.session() instead)
- Configuration goes in rxconfig.py as suplex={...} dict with keys: api_url, api_key, jwt_secret (optional for new Supabase APIs using JWKS), service_role, cookie_max_age, debug, let_jwt_expire
- Suplex is NOT installed yet in the project
About Apollo's Current State (Critical Issues Found)
1. Auth is broken end-to-end: sign_up_user() exists but is NEVER called in the UI flow. sign_in_user() is called but tokens are discarded after login. No session persistence.
2. State hierarchy is disconnected: AuthState(rx.State) and DBState(rx.State) are completely independent — AuthState has no DB access, ChatState has no auth context.
3. DB model/code mismatch: Messages model has question_encrypted/answer_encrypted columns (from migration 2), but DBState code references question/answer (old column names).
4. Alembic is broken: env.py has target_metadata = None, alembic.ini has placeholder URL driver://user:pass@localhost/dbname.
5. No user scoping: DBState.load_conversations_async() loads ALL conversations without WHERE user_id = ? filter.
6. Hardcoded user data: ChatState has user_name: str = "Bryan Nunez" and user_email: str = "b.nunez@hotmail.es".
7. No auth guards: /chat route has no protection — anyone can navigate directly to it.
About Reflex DB/Auth
- reflex db init initializes Alembic with correct metadata
- reflex db makemigrations --message '...' generates migration scripts
- reflex db migrate applies migrations
- Models must inherit from rx.Model (not raw SQLModel) for Reflex to detect them
- rx.Cookie and rx.LocalStorage persist state across sessions
- Backend-only vars (prefixed with _) are not sent to frontend — good for sensitive data
Accomplished
Completed
1. Toast component rewrite — Proyecto_Apollo/components/ui/toast.py was rewritten from individual functions returning rx.Component (buttons wrapping toasts) to a CustomToastWrapper class that returns rx.EventSpec. Supports toast(), toast.success(), toast.error(), toast.warning(), toast.info() with configurable message, description, bg_color, color, close_button, position, duration.
2. Updated __init__.py — Changed from exporting toast, toast_success, toast_error, toast_warning, toast_info to just exporting toast (the wrapper instance).
3. Updated testing_atoms.py — Fixed imports, fixed show_toast handler to use toast.success() instead of the old component, replaced individual toast component calls with button + on_click patterns.
4. Complete 5-phase plan for Suplex + reflex db integration — Fully researched, documented, and presented to user with architecture decisions confirmed.
NOT Yet Started (Next Steps — The 5-Phase Plan)
PHASE 1: Installation & Base Config (Adrian)
- Install suplex, update requirements.txt
- Add suplex={...} block to rxconfig.py
- Update .env with service role key if needed
- Remove supabase_client.py singleton
PHASE 2: Migrate Models to rx.Model + reflex db init (Jazmin)
- Delete current alembic/ directory and alembic.ini
- Convert models from SQLModel to rx.Model
- Move models from db/ to Proyecto_Apollo/models/
- Run reflex db init → reflex db makemigrations → reflex db migrate
PHASE 3: Restructure Auth with Suplex (Adrian + Jazmin review)
- Create AuthState(Suplex) inheriting from Suplex
- New state hierarchy: Suplex → AuthState → DBState → ChatState
- Wire up real sign_up, sign_in_with_password, log_out
- Add auth guards on /chat route
- Token persistence is automatic via Suplex's rx.Cookie
PHASE 4: Connect Auth with Data (User Scoping) (Jazmin + Adrian)
- Filter conversations by user_id from Suplex's self.user_id
- Assign user_id when creating conversations
- Sync Supabase Auth user with users table
- Remove hardcoded user data from ChatState
- Fix column name mismatch in Messages
PHASE 5: Cleanup, Testing & Documentation (Adrian + Giovann + PM)
- Delete db/engine.py, test files (test_db.py, etc.)
- Possibly remove supabase Python SDK dependency
- Full E2E testing of auth flow
- Update ATLAS documentation
Relevant files / directories
Apollo Project Root
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/rxconfig.py — Reflex config (needs suplex={...} block added)
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/.env — Environment variables (has SUPABASE_URL, SUPABASE_ANON_KEY, DATABASE_URL)
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/requirements.txt — Dependencies (suplex not yet added)
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/alembic.ini — Broken, to be deleted and regenerated
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/alembic/ — Broken migrations, to be deleted and regenerated
Database Layer (to be restructured)
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/db/ — Current models directory (to be moved to Proyecto_Apollo/models/)
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/db/engine.py — Custom SQLAlchemy engine (to be deleted)
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/db/db_state.py — DBState(rx.State) with conversation/message CRUD
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/db/users.py — Users model (SQLModel)
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/db/conversations.py — Conversations model (SQLModel)
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/db/messages.py — Messages model (SQLModel)
Auth Module
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/Proyecto_Apollo/modules/auth/state/auth_state.py — Current AuthState(rx.State), to become AuthState(Suplex)
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/Proyecto_Apollo/modules/auth/backend/supabase_client.py — Supabase singleton (to be removed)
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/Proyecto_Apollo/modules/auth/pages/auth_page.py — 6-step auth UI
Chat Module
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/Proyecto_Apollo/modules/chat/state/chat_state.py — ChatState(DBState) with hardcoded user data
Components (Modified in this session)
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/Proyecto_Apollo/components/ui/toast.py — MODIFIED: Rewritten as CustomToastWrapper class
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/Proyecto_Apollo/components/ui/__init__.py — MODIFIED: Updated exports
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/Proyecto_Apollo/modules/core/pages/testing_atoms.py — MODIFIED: Fixed toast usage
Config
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/Proyecto_Apollo/config/settings.py — Loads env vars
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/Proyecto_Apollo/Proyecto_Apollo.py — App entry point with routes
Styles
- /Users/bradrez/Documents/Atlas/atlas/projects/apollo/Proyecto_Apollo/styles/colors.py — ONANO brand color system (used by toast wrapper)
ATLAS Documentation
- /Users/bradrez/Documents/Atlas/atlas/docs/projects/apollo.md — Apollo project docs (needs update after changes)
- /Users/bradrez/Documents/Atlas/atlas/patterns/autenticacion.md — Auth patterns (needs update with Suplex patterns)
Agent Definitions
- /Users/bradrez/Documents/Atlas/atlas/.config/opencode/agents/project-manager.md
- /Users/bradrez/Documents/Atlas/atlas/.config/opencode/agents/jazmin-backend-architect.md
- /Users/bradrez/Documents/Atlas/atlas/.config/opencode/agents/adrian-senior-dev.md
Suplex Source (analyzed, not in project)
- /tmp/suplex_pkg/suplex-0.2.7-py3-none-any.whl — Downloaded wheel with full source code analyzed
▣  Compaction · claude-opus-4.6 · 1m 5s
Based on the comprehensive summary above, here's where we stand:
Current Status
Completed:
- Toast component rewrite (working CustomToastWrapper class)
- Full research on Suplex (v0.2.7) — source code analyzed
- Complete audit of Apollo's current state (7 critical issues identified)
- 5-phase integration plan designed with architecture decisions confirmed
Next up: Phase 1 of the Suplex + Reflex DB integration plan
The next logical step is to begin executing the 5-phase plan. Phase 1 involves:
1. Install suplex and update requirements.txt
2. Add suplex={...} config block to rxconfig.py
3. Update .env with any needed keys (e.g., JWT_SECRET, SERVICE_ROLE)
4. Remove the supabase_client.py singleton