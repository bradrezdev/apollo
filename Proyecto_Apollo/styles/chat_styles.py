"""Estilos para componentes de chat"""

import reflex as rx
from .colors import *
from .fonts import *
from ..components.ui import *

# === ESTILOS BASE ===
base_message_style = {
    "padding": "8px 16px",
    "border_radius": "26px",
    "display": "inline-block",
    "overflow_wrap": "break-word",
}

# === ESTILOS PARA MENSAJES ===
question_style = {
    **base_message_style,
    "background_color": rx.color_mode_cond(
        light=BRAND_BACKGROUND_ALT,
        dark=BRAND_BACKGROUND_ALT
    ),
    "color": rx.color_mode_cond(
        light=BRAND_TEXT_DARK,
        dark=BRAND_WHITE
    ),
    "margin_right": "10px",
    "max_width": "80%",
    "white_space": "pre-wrap",
}

answer_style = {
    **base_message_style,
    "max_width": "100%",
    "color": rx.color_mode_cond(
        light=BRAND_TEXT_DARK,
        dark=BRAND_WHITE
    ),
}

# === ESTILOS PARA CONTAINERS - DESKTOP ===
chat_container_desktop_style = {
    "width": "100dvw",
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
}

chat_scroll_mobile_style = {
    "scroll_behavior": "smooth",
}

# === ESTILOS PARA INPUT ===
chat_input_style = {
    "direction": "row",
    "margin_bottom": "2em",
    "spacing": "2",
    "width": "100%",
}

text_area_desktop_style = {
    #"rows": "1",
    "auto_height": True,
    "max_height": "150px",
    #"resize": "none",
    "placeholder": "Pregúntale a Onai…",
    "width": "100%",
    "variant": "soft",
    "bg": "transparent",
    "padding": "8px",
    "font_size": "1rem",
    "color": rx.color_mode_cond(
        light=BRAND_TEXT_DARK,
        dark=BRAND_WHITE
    ),
    "_focus": {
        "outline": "none",
        "box_shadow": "none",
        "bg": "transparent",
    },
}

text_area_mobile_style = {
    "auto_height": True,
    "max_height": "120px",
    "placeholder": "Pregúntale a Onai…",
    "width": "100%",
    "variant": "soft",
    "bg": "transparent",
    "padding": "6px",
    "input_mode": "text",
    "auto_capitalize": "sentences",
    "font_size": "16px",
    "border_radius": "14px",
    "color": rx.color_mode_cond(
        light=BRAND_TEXT_DARK,
        dark=BRAND_WHITE
    ),
}

send_button_desktop_style = {
    "bg": rx.color_mode_cond(
        light=BRAND_BACKGROUND_ALT,
        dark=BRAND_BACKGROUND_ALT
    ),
    "radius": "full",
    "size": "3",
    "_hover": {
        "bg": rx.color_mode_cond(
            light=BRAND_BACKGROUND_ALT,
            dark=BRAND_BACKGROUND_ALT
        ),
    },
}

send_button_mobile_style = {
    "bg": rx.color_mode_cond(
        light=BRAND_BACKGROUND_ALT,
        dark=BRAND_BACKGROUND_ALT
    ),
    "radius": "full",
    "size": "3",
    "_hover": {
        "bg": rx.color_mode_cond(
            light=BRAND_BACKGROUND_ALT,
            dark=BRAND_BACKGROUND_ALT
        ),
    },
}
