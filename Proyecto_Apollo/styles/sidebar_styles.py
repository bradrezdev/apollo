"""Estilos para componentes del sidebar"""

import reflex as rx
from .colors import ApolloTheme
from .common_styles import glassmorphism_style

# === ESTILOS PARA SIDEBAR ===
sidebar_style = {
    **glassmorphism_style,
    "border_radius": "24px",
    "display": ["none", "none", "flex", "flex", "flex"],
    "flex_direction": "column",
    "height": "95vh",
    "margin": "2.5vh 0 2.5vh 1rem",
    "max_width": "320px",
    "padding": "1.5rem",
    "width": "320px",
    "z_index": "1000",
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
    "src": "/logotipo.png",
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
