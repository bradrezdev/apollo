# Proyecto_Apollo.py
"""
Archivo principal de la aplicación Apollo - ChatBot con IA
Este archivo orquesta todos los componentes modulares para crear la interfaz del chat.
En el futuro, este archivo manejará el sistema de login antes de acceder al chat.
"""

import sys
print("[DEBUG] Cargando módulo Proyecto_Apollo.py", flush=True)

import reflex as rx
from Proyecto_Apollo.state import State

# Importar componentes modulares
from Proyecto_Apollo.components.chat import responsive_chat_container
from Proyecto_Apollo.components.sidebar import desktop_sidebar, edit_conversation_dialog, delete_conversation_dialog
from Proyecto_Apollo.components.layout.splash_screen import splash_screen

# === COMPOSICIÓN DE VISTAS ===

def unified_view() -> rx.Component:
    """Vista unificada y responsiva para todos los dispositivos"""
    return rx.flex(
        # Sidebar se muestra/oculta automáticamente mediante CSS (breakpoints) definidos en sus estilos
        desktop_sidebar(),
        
        # Área principal de Chat
        rx.box(
            responsive_chat_container(),
            flex="1",
            width="100%",
            height="100%",
            position="relative",
            overflow="hidden",
        ),
        
        # Propiedades del contenedor principal — fixed para bloquear viewport en iOS
        width="100%",
        height="100dvh",
        flex_direction="row",
        align_items="stretch",
        overflow="hidden",
        position="fixed",
        top="0",
        left="0",
    )


def index() -> rx.Component:
    """Punto de entrada principal - Renderiza vista unificada"""
    return rx.fragment(
        splash_screen(),
        unified_view(),
        edit_conversation_dialog(),
        delete_conversation_dialog(),
    )


# === CONFIGURACIÓN DE LA APLICACIÓN ===

head_config = [
    # Enlace al manifest para PWA
    rx.el.link(
        rel="manifest",
        href="manifest.json"
    ),

    # Icono para iOS (Safari)
    rx.el.link(
        rel="apple-touch-icon",
        href="apple-touch-icon.png"
    ),
],

 # Meta tags para PWA, SEO y redes sociales
meta = [
    # Evitar zoom automático en inputs (maximum-scale=1, user-scalable=no)
    {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover, interactive-widget=resizes-content"},
    {"name": "apple-mobile-web-app-status-bar-style", "content": "black-translucent"}, 
    {"name": "apple-mobile-web-app-capable", "content": "yes"},
    {"name": "theme-color", "content": "#062A63"},
    
    # --- SEO & DESCRIPTION ---
    {"name": "description", "content": "ONANO | Nanotecnología aplicada al bienestar y la libertad financiera. Únete a la revolución de la nanotecnología y proyecta tu éxito."},
    {"name": "keywords", "content": "nanotecnología, bienestar, simulador financiero, onano, red de mercadeo, salud, tecnología cuántica"},
    {"name": "author", "content": "ONANO Global"},

    # --- OPEN GRAPH (Facebook, WhatsApp, LinkedIn) ---
    {"property": "og:type", "content": "website"},
    {"property": "og:url", "content": "https://onano-web-teal-apple.reflex.run"}, # URL placeholder
    {"property": "og:title", "content": "ONANO | Proyecta tu Éxito"},
    {"property": "og:description", "content": "Innovación en bienestar y libertad financiera. Descubre el futuro de la nanotecnología."},
    {"property": "og:image", "content": "https://onano-web-teal-apple.reflex.run/light-logo.svg"},
]

# Estilos globales para forzar comportamiento en móviles
global_styles = {
    "html, body": {
        "height": "100dvh",
        "overflow": "hidden",
        "overscroll-behavior": "none",
    },
    "@media screen and (max-width: 480px)": {
        "textarea, input": {
            "font-size": "16px !important",
        }
    }
}

app = rx.App(
    style=global_styles,
    theme=rx.theme(
        appearance="inherit",
    ),
)

app.add_page(index, title="Apollo AI - ChatBot con IA", on_load=State.on_load)