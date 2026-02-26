import reflex as rx
from ...styles.colors import *
from ...styles import fonts

def atom_toast(message: str, type: str = "info", **kwargs) -> rx.Component:
    """Toast atómico para notificaciones."""
    bg_color = BRAND_INFO if type == "info" else BRAND_SUCCESS if type == "success" else BRAND_ERROR
    return rx.box(
        rx.hstack(
            rx.icon("info", color=BRAND_WHITE, size=20),
            rx.text(message, color=BRAND_WHITE, font_weight="bold"),
            spacing="3",
            align="center"
        ),
        bg=bg_color,
        padding="16px",
        border_radius="8px",
        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
        **kwargs
    )
