"""Estilos para componentes del sidebar"""

from .colors import WHITE, ACCENT_LIGHT, ACCENT_DARK

# === ESTILOS PARA SIDEBAR ===
sidebar_style = {
    "bg": WHITE,
    "padding": "1rem",
    "height": "100vh",
    "width": "220px",
}

sidebar_item_hover_style = {
    "_hover": {
        "bg": ACCENT_LIGHT,
        "color": ACCENT_DARK,
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
