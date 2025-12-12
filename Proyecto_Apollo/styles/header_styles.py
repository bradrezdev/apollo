"""Estilos para componentes del header"""

import reflex as rx
from .colors import ApolloTheme

# === TAMAÑOS DE ICONOS ===
icon_sizes = {
    "small": 24,
    "medium": 28,
    "large": 30,
}

# === ESTILOS PARA HEADER DESKTOP ===
header_desktop_style = {
    "position": "fixed",
    "top": 0,
    "z_index": 100,
    "bg": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["header_background"],
        dark=ApolloTheme.dark_colors()["header_background"]
    ),
    "style": {
        "backdropFilter": "blur(60px)",
        "-webkit-backdrop-filter": "blur(60px)",
    },
    "height": "8vh",
    "width": "85%",
}

title_style = {
    "align": "center",
    "weight": "bold",
    "color": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["header_text_color"],
        dark=ApolloTheme.dark_colors()["header_text_color"]
    ),
}

# === ESTILOS PARA HEADER MOBILE ===
header_mobile_gradient_style = {
    "background": "linear-gradient(to bottom, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0))",
    "height": "4rem",
    "position": "fixed",
    "top": 0,
    "width": "100%",
    "z_index": 100,
    "display": "flex",
    "align_items": "center",
}

header_mobile_content_style = {
    "align": "center",
    "height": "100%",
    "justify": "between",
    "padding_left": "4%",
    "padding_right": "4%",
    "width": "100%",
}

# Estilos para los boxes dentro del header mobile
header_mobile_box_style = {
    "bg": "rgba(25, 25, 25, 0.35)",
    "style": {
        "backdropFilter": "blur(30px)",
        "-webkit-backdrop-filter": "blur(30px)",
    },
}

header_mobile_round_box_style = {
    **header_mobile_box_style,
    "border_radius": "50%",
    "padding": "1rem",
}

header_mobile_title_box_style = {
    **header_mobile_box_style,
    "border_radius": "50px",
    "padding_x": "1.5rem",
    "padding_y": "0.75rem",
}

mobile_title_style = {
    "align": "center",
    "color": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["header_icon_color"],
        dark=ApolloTheme.dark_colors()["header_icon_color"]
    ),
    "size": "4",
}

# === ESTILOS PARA DRAWER ===
drawer_trigger_style = {
    "size": icon_sizes["medium"],
}

drawer_content_style = {
    "top": "auto",
    "right": "auto",
    "height": "100%",
    "width": "20em",
    "padding": "1.5em",
    "bg": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["sidebar_background"],
        dark=ApolloTheme.dark_colors()["sidebar_background"]
    ),
}

# === ESTILOS COMPARTIDOS CON SIDEBAR ===
user_name_style = {
    "size": "3",
    "weight": "bold",
}
