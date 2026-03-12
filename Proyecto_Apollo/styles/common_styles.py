"""Estilos comunes reutilizables en toda la aplicación"""

import reflex as rx
from .colors import *

# === EFECTOS VISUALES ===
glassmorphism_style = {
    "bg": rx.color_mode_cond(
        light=BRAND_BACKGROUND_ALT,
        dark=BRAND_BACKGROUND_ALT
    ),
    "border": rx.color_mode_cond(
        light=f"1px solid {BRAND_BACKGROUND_ALT}",
        dark=f"1px solid {BRAND_BACKGROUND_ALT}",
    ),
    "box_shadow": rx.color_mode_cond(
        light=f"{BRAND_BACKGROUND_ALT}10 4px 30px",
        dark=f"{BRAND_BACKGROUND_ALT}10 4px 30px",
    ),
    "style": {
        "backdropFilter": "blur(20px)",
        "-webkit-backdrop-filter": "blur(20px)",
    },
}
