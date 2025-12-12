"""Estilos para componentes de chat"""

from .colors import GRAY_DARK

# === ESTILOS BASE ===
base_message_style = {
    "padding": "2vh",
    "border_radius": "20px",
    "display": "inline-block",
    "overflow_wrap": "break-word",
    "white_space": "pre-wrap",
}

# === ESTILOS PARA MENSAJES ===
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
    "height": "50%",
    "overflow_y": "hidden",
    "padding_top": "4rem",
    "padding_bottom": "1rem",
    "z_index": 1,
}

chat_scroll_mobile_style = {
    "height": "50%",
    "scroll_behavior": "smooth",
    "width": "100%",
}

# === ESTILOS PARA INPUT ===
chat_input_style = {
    "bg": "rgba(255, 255, 255, 0.35)",
    "border_radius": "16px",
    "direction": "row",
    "margin_left": "2%",
    "padding": "3%",
    "spacing": "2",
    "style": {
        "backdropFilter": "blur(60px)",
        "-webkit-backdrop-filter": "blur(60px)",
    },
    "width": "96%",
}

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

send_button_desktop_style = {
    "bg": "#0984e3",
    "radius": "full",
    "size": "3",
}

send_button_mobile_style = {
    "bg": "#0984e3",
    "radius": "full",
    "size": "3",
}
