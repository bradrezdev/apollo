"""Estilos para componentes del sidebar"""

import reflex as rx
from .colors import ApolloTheme

# === ESTILOS PARA SIDEBAR ===
sidebar_style = {
    "bg": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["sidebar_background"],
        dark=ApolloTheme.dark_colors()["sidebar_background"]
    ),
    "padding": "1.5rem",
    "height": "100vh",
    "width": "280px",
    "border_right": rx.color_mode_cond(
        light="1px solid #E5E7EB",
        dark="1px solid #2C2C2E",
    ),
    "display": ["none", "none", "flex", "flex", "flex"],
    "flex_direction": "column",
}

sidebar_item_hover_style = {
    "transition": "all 0.2s ease",
    "color": rx.color_mode_cond(
        light="#4B5563",
        dark="#D1D5DB",
    ),
    "_hover": {
        "bg": rx.color_mode_cond(
            light=ApolloTheme.light_colors()["sidebar_item_hover"],
            dark=ApolloTheme.dark_colors()["sidebar_item_hover"]
        ),
        "color": rx.color_mode_cond(
            light=ApolloTheme.light_colors()["accent"],
            dark="#FFFFFF",
        ),
        "cursor": "pointer",
        "transform": "translateX(4px)",
    },
    "border-radius": "8px",
}

# === ESTILOS PARA LOGO ===
logo_style = {
    "src": "/logoNNprotect.png",
    "height": "auto",
    "margin_bottom": "1em",
    "width": "100%",
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
