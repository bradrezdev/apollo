"""Estilos comunes reutilizables en toda la aplicación"""

import reflex as rx
from .colors import ApolloTheme

# === EFECTOS VISUALES ===
glassmorphism_style = {
    "bg": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["input_background"],
        dark=ApolloTheme.dark_colors()["input_background"]
    ),
    "border": rx.color_mode_cond(
        light=f"1px solid {ApolloTheme.light_colors()['input_border']}",
        dark="1px solid rgba(255, 255, 255, 0.1)",
    ),
    "box_shadow": rx.color_mode_cond(
        light=ApolloTheme.light_colors()["box_shadow"],
        dark="0 4px 20px rgba(0, 0, 0, 0.4)",
    ),
    "style": {
        "backdropFilter": "blur(20px)",
        "-webkit-backdrop-filter": "blur(20px)",
    },
}
