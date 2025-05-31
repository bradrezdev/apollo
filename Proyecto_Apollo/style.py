# style.py

import reflex as rx

# === CONSTANTES DE DISEÑO GLOBAL ===
PRIMARY_BG = "#FFFFFF"
ACCENT_COLOR = rx.color("accent", 2)
ACCENT_LIGHT = rx.color("accent", 4)
ACCENT_DARK = rx.color("accent", 11)

# Colores adicionales
WHITE = "#FFFFFF"
BLUE_PRIMARY = "#0080ff"
GRAY_DARK = "#595959"

# === ESTILOS BASE ===
base_message_style = {
    "padding": "2vh",
    "border_radius": "20px",
    "display": "inline-block",
    "overflow_wrap": "break-word",
    "white_space": "pre-wrap",
}

# === ESTILOS PARA CHAT ===
chat_margin = "40%"

question_style = {
    **base_message_style,
    "background_color": GRAY_DARK,
    "margin_left": chat_margin,
    "margin_right": "16px",
    "max_width": "58.6%",
}

answer_style = {
    **base_message_style,
    "margin_left": "16px",
}

# Estilos para chat container - Desktop
chat_container_desktop_style = {
    "spacing": "0",
    "width": "100vw",
}

chat_scroll_desktop_style = {
    "height": "100%",
    "overflow_y": "scroll",
    "scroll_behavior": "smooth",
    "width": "100%",
}

# Estilos para chat container - Mobile
chat_container_mobile_style = {
    "flex": "1",
    "width": "100%",
    "height": "100%",
    "overflow_y": "auto",
    "padding_top": "4rem",  # Espacio para el header
    "padding_bottom": "1rem",  # Espacio para el input
    "z_index": 1,
}

chat_scroll_mobile_style = {
    "height": "100%",
    "overflow_y": "auto",
    "scroll_behavior": "smooth",
    "width": "100%",
    "min_height": "100%",
}

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

# === ESTILOS PARA HEADER ===
header_desktop_style = {
    "position": "fixed",
    "top": 0,
    "z_index": 100,
    "bg": "rgba(255, 255, 255, 0.35)",
    "style": {
        "backdropFilter": "blur(60px)",
        "-webkit-backdrop-filter": "blur(60px)",
    },
    "height": "8vh",
    "width": "85%",
}

header_mobile_style = {
    "bg": "rgba(255, 255, 255, 0.35)",
    "height": "4rem",
    "justify": "between",
    "padding_left": "4%",
    "padding_right": "4%",
    "position": "fixed",
    "top": 0,
    "style": {
        "backdropFilter": "blur(10px)",
        "-webkit-backdrop-filter": "blur(10px)",
    },
    "width": "100%",
    "z_index": 100,
}

header_mobile_gradient_style = {
    "background": "linear-gradient(to bottom, rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0))",
    "height": "4rem",
    "position": "fixed",
    "top": 0,
    "width": "100%",
    "z_index": 100,
    "display": "flex",
    "align_items": "center",
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

header_mobile_content_style = {
    "align": "center",
    "width": "100%",
    "height": "100%",
    "padding_x": "1rem",
}

# === ESTILOS PARA INPUTS ===
text_area_desktop_style = {
    "rows": "3",
    "resize": "none",
    "placeholder": "Pregunta lo que quieras",
    "width": "100%",
}

text_area_mobile_style = {
    "max_length": 150,
    "rows": "1",
    "resize": "vertical",
    "placeholder": "Pregunta lo que quieras",
    "width": "100%",
}

chat_input_style = {
    "bg": "rgba(255, 255, 255, 0.35)",
    "border_radius": "16px",
    "direction": "row",
    "justify": "end",
    "margin_bottom": "4%",
    "margin_left": "2%",
    "padding": "3%",
    "position": "fixed",
    "bottom": 0,
    "spacing": "2",
    "style": {
        "backdropFilter": "blur(60px)",
        "-webkit-backdrop-filter": "blur(60px)",
    },
    "width": "96%",
    "z_index": 10,
}

# === ESTILOS PARA BOTONES ===
send_button_desktop_style = {
    "bg": BLUE_PRIMARY,
    "radius": "full",
    "size": "3",
}

send_button_mobile_style = {
    "bg": WHITE,
    "radius": "full",
    "size": "2",
}

# === ESTILOS PARA DRAWER ===
drawer_content_style = {
    "top": "auto",
    "right": "auto",
    "height": "100%",
    "width": "20em",
    "padding": "1.5em",
    "bg": ACCENT_COLOR,
}

drawer_trigger_style = {
    "size": 20,
    "color": WHITE,
}

drawer_close_style = {
    "size": 30,
}

# === ESTILOS PARA IMÁGENES ===
banner_desktop_style = {
    "border_radius": "16px",
    "width": "100%",
    "height": "100%",
    "style": {"objectFit": "cover"},
}

banner_mobile_style = {
    "border_radius": "16px",
    "width": "100%",
    "height": "100%",
    "style": {"objectFit": "cover"},
}

logo_style = {
    "src": "/logoNNprotect.png",
}

# === ESTILOS PARA LAYOUTS ===
desktop_layout_style = {
    "height": "85vh",
    "overflow_y": "auto",
    "max_width": "100%",
    "margin_bottom": "1vh",
    "min_width": "50%",
}

mobile_layout_style = {
    "direction": "column",
    "height": "100vh",
    "width": "100%",
    "position": "relative",
}

main_container_style = {
    "flex": "1",
    "background_color": PRIMARY_BG,
    "min_height": "0",
    "height": "100%",
    "width": "100%",
}

# === ESTILOS PARA ICONOS ===
icon_sizes = {
    "small": 20,
    "medium": 20,
    "large": 20,
}

# === ESTILOS PARA TEXTO ===
title_style = {
    "align": "center",
    "weight": "bold",
}

user_name_style = {
    "size": "3",
    "weight": "bold",
}

user_email_style = {
    "size": "1", 
    "weight": "medium",
}

mobile_title_style = {
    "align": "center",
    "color": WHITE,
    "size": "10",
    "weight": "Bold",
}

# === ESTILOS PARA CONTENEDORES ===
banner_container_desktop_style = {
    "height": "16vh",
    "margin_top": "9vh",
    "width": "98%",
}

banner_container_mobile_style = {
    "width": "100%",
    "padding": "1rem",
    "margin_top": "1rem",
}

user_info_container_style = {
    "width": "100%",
}

# Contenedor principal del chat mobile
mobile_chat_main_container_style = {
    "height": "100vh",
    "width": "100%",
    "overflow": "hidden",
    "position": "relative",
}