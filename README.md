# 🚀 Proyecto Apollo - Asistente Virtual Inteligente

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Reflex](https://img.shields.io/badge/Reflex-0.8.22-purple.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-Assistants-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-orange.svg)

**Un chatbot inteligente construido con Reflex y OpenAI Assistants API, modular y escalable.**

</div>

---

## 📋 Descripción

**Proyecto Apollo** es una aplicación de chat de última generación construida con **Reflex** (framework Full-Stack para Python). Integra la potencia de **OpenAI Assistants API** para ofrecer respuestas inteligentes y contextuales, respaldada por una base de datos **PostgreSQL** (vía Supabase) para una persistencia de datos robusta.

Este proyecto ha sido diseñado siguiendo principios de **Clean Architecture** y **SOLID**, garantizando un código mantenible, escalable y profesional.

---

## ✨ Características Principales

El sistema cuenta con un conjunto robusto de funcionalidades diseñadas para ofrecer la mejor experiencia de usuario:

- 🤖 **Inteligencia Artificial Avanzada**: Integración directa con OpenAI Assistants para conversaciones fluidas y con contexto.
- 🗂️ **Historial Persistente**: Almacenamiento seguro de todas las conversaciones y mensajes en base de datos.
- 📱 **Diseño Responsive (Mobile-First)**: Interfaz optimizada que se adapta perfectamente a dispositivos móviles y de escritorio.
- ✏️ **Gestión de Conversaciones**:
  - Creación de nuevos chats instantáneos.
  - Edición de títulos de conversación para mejor organización.
  - Eliminación de conversaciones obsoletas.
- 🔄 **Continuidad de Sesión**: Capacidad para retomar cualquier conversación antigua en el punto exacto donde se dejó.
- 🎨 **UI/UX Moderna**: Interfaz limpia, intuitiva y con feedback visual en tiempo real (streaming de respuestas).

---

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

- **Python 3.13** o superior.
- **Git** para el control de versiones.
- Una cuenta en **OpenAI** (con API Key y Assistant ID).
- Una cuenta en **Supabase** (o una base de datos PostgreSQL local).

---

## 🚀 Guía de Instalación y Ejecución

Sigue estos pasos para desplegar el proyecto en tu entorno local.

### 1. Clonar el Repositorio

```bash
git clone https://github.com/HyEd-IA/llm-bradrezdev.git
cd Proyecto_Apollo
```

### 2. Configurar el Entorno Virtual

Es **indispensable** crear un entorno virtual para aislar las dependencias del proyecto.

**En macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**En Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar Dependencias

Con el entorno virtual activo, instala todas las librerías necesarias listadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Ejecución (Modo Rápido)

El proyecto viene pre-configurado con credenciales de demostración. Una vez instaladas las dependencias, **no es necesario configurar nada más**.

Simplemente inicia la aplicación:

```bash
reflex run
```

La aplicación estará disponible en `http://localhost:3000`.

---

### ⚙️ Configuración Personalizada (Opcional)

Si deseas conectar tu propia infraestructura de OpenAI y Supabase:

1. **Configurar Variables de Entorno**:
   Crea un archivo `.env` en la raíz y define tus credenciales:
   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=sk-tu-api-key-aqui
   API_ASSISTANT_ID=asst_tu-assistant-id-aqui

   # Supabase / Database Configuration
   SUPABASE_URL=https://tu-proyecto.supabase.co
   SUPABASE_KEY=tu-supabase-anon-key
   # Usa la URL del Connection Pooler (puerto 5432 + tenant) para evitar errores IPv6
   DATABASE_URL=postgresql://postgres.tu-proyecto:password@aws-0-REGION.pooler.supabase.com:5432/database
   ```
   > ⚠️ **Nota importante sobre Supabase:** Usa la URL del **Connection Pooler** en modo **Session** (como se muestra arriba) en lugar de la URL directa (`db...supabase.co`). Esto evita errores de timeout (`psycopg2.OperationalError`) causados por la falta de soporte IPv6 nativo en algunos entornos de desarrollo locales.

2. **Inicializar Base de Datos**:
   Si usas tu propia BD, ejecuta las migraciones:
   ```bash
   reflex db migrate
   ```

3. **Ejecutar**:
   ```bash
   reflex run
   ```

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una estructura modular para facilitar el mantenimiento y la escalabilidad:

```text
Proyecto_Apollo/
├── Proyecto_Apollo.py          # 🚪 Punto de entrada (Entry Point)
├── state.py                    # 🧠 Lógica de negocio y Estado de la UI
├── components/                 # 🧩 Componentes UI Reutilizables
│   ├── chat/                   # Componentes del área de chat
│   ├── sidebar/                # Barra lateral y gestión de historial
│   ├── header/                 # Encabezados y navegación
│   └── ...
├── styles/                     # 🎨 Sistema de Diseño y Estilos
├── config/                     # ⚙️ Configuraciones globales
└── db/                         # 🗄️ Capa de Datos (Modelos y CRUD)
```

---

## 💻 Tecnologías Utilizadas

- **Frontend & Backend**: [Reflex](https://reflex.dev) (Python)
- **Base de Datos**: PostgreSQL, SQLModel, Alembic
- **IA / LLM**: OpenAI API (Assistants)
- **Infraestructura**: Supabase

---

## 📄 Licencia

MIT License

Copyright (c) 2025 Bryan Núñez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.