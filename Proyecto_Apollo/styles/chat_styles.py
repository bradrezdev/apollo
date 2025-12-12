"""Estilos para componentes de chat"""

import reflex as rx
from .colors import ApolloTheme

# === ESTILOS BASE ===
base_message_style = {
    "padding": "8px 16px 8px 16px",
    "border_radius": "26px",
    "display": "inline-block",
    "overflow_wrap": "break-word",
}

# === ESTILOS PARA MENSAJES ===
chat_margin = "0%"

question_style = {
    **base_message_style,
    "background_color": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["question_background"],
        dark=ApolloTheme.dark_colors()["question_background"]
    ),
    "color": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["question_text_color"],
        dark=ApolloTheme.dark_colors()["question_text_color"]
    ),
    "margin_left": chat_margin,
    "margin_right": "10px",
    "max_width": "80%",
    "white_space": "pre-wrap",
}

answer_style = {
    **base_message_style,
    "margin_left": "10px",
    "max_width": "100%",
    "color": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["answer_text_color"],
        dark=ApolloTheme.dark_colors()["answer_text_color"]
    ),
}

# === ESTILOS PARA CONTAINERS - DESKTOP ===
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

# === ESTILOS PARA CONTAINERS - MOBILE ===
chat_container_mobile_style = {
    "width": "100%",
    "flex": "1",  # Ocupa todo el espacio disponible
    "overflow_y": "auto",  # Cambiar a auto para permitir scroll
    "padding_top": "5rem",  # Espacio para el header flotante
    "padding_bottom": "1rem",
    "z_index": 1,
}

chat_scroll_mobile_style = {
    "height": "100%",
    "scroll_behavior": "smooth",
    "width": "100%",
}

# === ESTILOS PARA INPUT ===
chat_input_style = {
    "direction": "row",
    "margin_bottom": "2em",
    "spacing": "2",
    "width": "100%",
}

text_area_desktop_style = {
    "rows": "3",
    "resize": "none",
    "placeholder": "Pregunta lo que quieras",
    "width": "100%",
    "color": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["input_text_color"],
        dark=ApolloTheme.dark_colors()["input_text_color"]
    ),
}

text_area_mobile_style = {
    "max_length": 150,
    "rows": "1",
    "resize": "vertical",
    "placeholder": "Pregunta lo que quieras",
    "width": "100%",
    "color": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["input_text_color"],
        dark=ApolloTheme.dark_colors()["input_text_color"]
    ),
}

send_button_desktop_style = {
    "bg": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["send_button_color"],
        dark=ApolloTheme.dark_colors()["send_button_color"]
    ),
    "radius": "full",
    "size": "3",
    "_hover": {
        "bg": rx.color_mode_cond(
            light=ApolloTheme.light_colors()["send_button_hover_color"],
            dark=ApolloTheme.dark_colors()["send_button_hover_color"]
        ),
    },
}

send_button_mobile_style = {
    "bg": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["send_button_color"],
        dark=ApolloTheme.dark_colors()["send_button_color"]
    ),
    "radius": "full",
    "size": "3",
    "_hover": {
        "bg": rx.color_mode_cond(
            light=ApolloTheme.light_colors()["send_button_hover_color"],
            dark=ApolloTheme.dark_colors()["send_button_hover_color"]
        ),
    },
}
