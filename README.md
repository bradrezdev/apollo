# 🚀 Proyecto Apollo - Chatbot con IA

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Reflex](https://img.shields.io/badge/Reflex-0.7.11-purple.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-Assistants-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-orange.svg)

Un chatbot inteligente construido con Reflex y OpenAI Assistants API, con arquitectura modular y clean code.

[Demo](#) • [Documentación](ARCHITECTURE.md) • [Instalación](#-instalación)

</div>

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Arquitectura](#-arquitectura)
- [Desarrollo](#-desarrollo)
- [Roadmap](#-roadmap)

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

## 🏗️ Arquitectura

Este proyecto sigue una arquitectura modular basada en **principios SOLID** y **clean code**.

### Estructura de Directorios

```
Proyecto_Apollo/
├── Proyecto_Apollo.py          # Punto de entrada
├── state.py                    # Lógica de chat
├── components/                 # Componentes UI
│   ├── chat/                   # Componentes de mensajes
│   ├── sidebar/                # Navegación e historial
│   ├── header/                 # Encabezados
│   └── layout/                 # Componentes estructurales
├── styles/                     # Sistema de estilos
│   ├── colors.py               # Paleta de colores
│   ├── chat_styles.py
│   ├── sidebar_styles.py
│   └── ...
├── config/                     # Configuración
│   └── settings.py             # API keys y constantes
└── db/                         # Capa de datos
    ├── conversations.py        # Modelo
    └── db_state.py             # Operaciones BD
```

Para una **guía completa de arquitectura**, consulta [ARCHITECTURE.md](ARCHITECTURE.md).

### Principios de Diseño

- **KISS**: Keep It Simple, Stupid
- **DRY**: Don't Repeat Yourself
- **YAGNI**: You Aren't Gonna Need It
- **POO**: Programación Orientada a Objetos

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

### Agregar una Nueva Feature

1. Lee [ARCHITECTURE.md](ARCHITECTURE.md) completo
2. Identifica en qué módulo va tu feature
3. Crea el componente en la carpeta correcta
4. Define estilos en `styles/`
5. Agrega lógica en `state.py` o `db_state.py`
6. Actualiza `__init__.py` para exports
7. Integra en el layout principal
8. Prueba en desktop Y móvil

**Consulta la sección "Cómo Agregar Nuevas Features" en [ARCHITECTURE.md](ARCHITECTURE.md) para un ejemplo completo.**

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

## 📚 Recursos

- [Reflex Documentation](https://reflex.dev/docs)
- [OpenAI Assistants Guide](https://platform.openai.com/docs/assistants)
- [Supabase Quickstart](https://supabase.com/docs/guides/getting-started)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

**Antes de contribuir, lee [ARCHITECTURE.md](ARCHITECTURE.md) para entender la estructura del proyecto.**

---

## 👤 Autor

**BradRez**

- GitHub: [@bradrezdev](https://github.com/bradrezdev)

---

## 🙏 Agradecimientos

- [Reflex](https://reflex.dev) - Por el increíble framework
- [OpenAI](https://openai.com) - Por la API de Assistants
- [Supabase](https://supabase.com) - Por la infraestructura de BD

---

<div align="center">

**Hecho con ❤️ y Python**

[⬆️ Volver arriba](#-proyecto-apollo---chatbot-con-ia)

</div>
