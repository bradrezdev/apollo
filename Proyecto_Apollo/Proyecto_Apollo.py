# Proyecto_Apollo.py
"""
Archivo principal de la aplicación Apollo - ChatBot con IA
Este archivo orquesta todos los componentes modulares para crear la interfaz del chat.
En el futuro, este archivo manejará el sistema de login antes de acceder al chat.
"""

import sys
print("[DEBUG] Cargando módulo Proyecto_Apollo.py", flush=True)

import reflex as rx

# Import models so reflex detects them
import Proyecto_Apollo.models


# Importar páginas
from Proyecto_Apollo.modules.auth.pages.auth_page import auth_page_ui
from Proyecto_Apollo.modules.auth.pages.confirm_page import confirm_page_ui
from Proyecto_Apollo.modules.auth.state.auth_state import AuthState
from Proyecto_Apollo.modules.auth.state.confirm_state import ConfirmState
from Proyecto_Apollo.modules.chat.pages.chat_page import chat_page
from Proyecto_Apollo.modules.chat.state.chat_state import State
from Proyecto_Apollo.modules.core.pages.testing_atoms import testing_atoms_page

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

app.add_page(auth_page_ui, route="/", title="Bienvenido a Apollo", on_load=AuthState.on_load)
app.add_page(confirm_page_ui, route="/confirm", title="Cuenta confirmada - Apollo", on_load=ConfirmState.on_load)
app.add_page(chat_page, route="/chat", title="Apollo AI - ChatBot con IA", on_load=State.on_load)
app.add_page(testing_atoms_page, route="/testing-atoms", title="Testing Átomos UI")
