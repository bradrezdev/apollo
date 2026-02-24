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
from Proyecto_Apollo.components.header.header_components import mobile_header

# === COMPOSICIÓN DE VISTAS ===

def unified_view() -> rx.Component:
    """Vista unificada y responsiva para todos los dispositivos"""
    return rx.flex(
        # Mobile header — absolute dentro del contenedor fixed para anclarse al --app-height
        rx.box(
            mobile_header(),
            display=["block", "block", "none", "none"],
            position="absolute",
            top="0",
            left="0",
            width="100%",
            z_index="1000",
        ),
        
        desktop_sidebar(),
        
        rx.box(
            responsive_chat_container(),
            flex="1",
            width="100%",
            height="100%",
            position="relative",
            overflow="hidden",
        ),
        
        width="100%",
        height="var(--app-height, 100dvh)",
        flex_direction="row",
        align_items="stretch",
        overflow="hidden",
        position="fixed",
        top="0",
        left="0",
    )


def index() -> rx.Component:
    """Punto de entrada principal - Renderiza vista unificada"""
    return rx.box(
        # Script para bloquear scroll global en iOS y ajustar altura al teclado
        rx.script("""
            // === 1. Bloquear touchmove fuera del chat ===
            document.addEventListener('touchmove', function(e) {
                let node = e.target;
                while (node && node !== document.body) {
                    if (node.classList && node.classList.contains('chat-scroll-area')) {
                        return;
                    }
                    node = node.parentNode;
                }
                e.preventDefault();
            }, { passive: false });

            // === 2. Ajustar --app-height con visualViewport ===
            function setAppHeight() {
                var vh = window.visualViewport ? window.visualViewport.height : window.innerHeight;
                document.documentElement.style.setProperty('--app-height', vh + 'px');
            }
            setAppHeight();
            if (window.visualViewport) {
                window.visualViewport.addEventListener('resize', setAppHeight);
                window.visualViewport.addEventListener('scroll', function() {
                    // Forzar scroll del viewport a 0 para evitar que iOS mueva la página
                    window.scrollTo(0, 0);
                });
            }
            window.addEventListener('resize', setAppHeight);
        """),
        splash_screen(),
        unified_view(),
        edit_conversation_dialog(),
        delete_conversation_dialog(),
        height="var(--app-height, 100dvh)",
        overflow="hidden",
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
        "height": "var(--app-height, 100dvh)",
        "overflow": "hidden",
        "overscroll-behavior": "none",
        "position": "fixed",
        "width": "100%",
        "touch-action": "none",
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