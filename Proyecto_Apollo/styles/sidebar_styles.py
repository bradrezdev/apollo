"""Estilos para componentes del sidebar"""

import reflex as rx
from .colors import ApolloTheme

# === ESTILOS PARA SIDEBAR ===
sidebar_style = {
    "bg": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["sidebar_background"],
        dark=ApolloTheme.dark_colors()["sidebar_background"]
    ),
    "padding": "1rem",
    "height": "100vh",
    "width": "220px",
}

sidebar_item_hover_style = {
    "_hover": {
        "bg": rx.color_mode_cond(
            light=ApolloTheme.light_colors()["sidebar_item_hover"],
            dark=ApolloTheme.dark_colors()["sidebar_item_hover"]
        ),
        "cursor": "pointer",
    },
    "border-radius": "0.5em",
}

# === ESTILOS PARA LOGO ===
logo_style = {
    "src": "/logoNNprotect.png",
    "width": "100%",
    "height": "auto",
}

# === ESTILOS PARA PERFIL DE USUARIO ===
user_name_style = {
    "size": "3",
    "weight": "bold",
}

user_email_style = {
    "size": "1",
    "weight": "medium",
}

user_info_container_style = {
    "width": "100%",
}
