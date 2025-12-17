# Proyecto_Apollo.py
"""
Archivo principal de la aplicación Apollo - ChatBot con IA
Este archivo orquesta todos los componentes modulares para crear la interfaz del chat.
En el futuro, este archivo manejará el sistema de login antes de acceder al chat.
"""

import reflex as rx
from Proyecto_Apollo.state import State

# Importar componentes modulares
from Proyecto_Apollo.components.chat import (
    chat_container_desktop,
    chat_container_mobile,
    desktop_chat_input,
    mobile_chat_input,
)
from Proyecto_Apollo.components.sidebar import desktop_sidebar, edit_conversation_dialog, delete_conversation_dialog
from Proyecto_Apollo.components.header import desktop_header, mobile_header


# === COMPOSICIÓN DE VISTAS ===

def desktop_view() -> rx.Component:
    """Vista principal para desktop con sidebar y chat"""
    return rx.flex(
        desktop_sidebar(),
        rx.vstack(
            chat_container_desktop(),
            desktop_chat_input(),
            width="100%",
            height="100dvh",
        ),
        width="100%",
        height="100dvh",
    )


def mobile_view() -> rx.Component:
    """Vista principal para mobile con drawer"""
    return rx.vstack(
        mobile_header(),
        chat_container_mobile(),
        mobile_chat_input(),
        spacing="0",
        width="100%",
        height="100vh",
    )


def index() -> rx.Component:
    """Punto de entrada principal - Renderiza vista según el dispositivo"""
    return rx.fragment(
        rx.desktop_only(desktop_view()),
        rx.mobile_only(mobile_view()),
        edit_conversation_dialog(),
        delete_conversation_dialog(),
    )


# === CONFIGURACIÓN DE LA APLICACIÓN ===

app = rx.App(
    theme=rx.theme(
        appearance="inherit",
    ),
)

app.add_page(index, title="Apollo AI - ChatBot con IA", on_load=State.on_load)
