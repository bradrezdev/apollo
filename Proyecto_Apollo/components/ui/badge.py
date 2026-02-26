import reflex as rx
from ...styles.colors import *
from ...styles import fonts

def atom_badge(text: str, is_valid: rx.Var[bool], **kwargs) -> rx.Component:
    """Badge atómico para mostrar estados como validaciones."""
    return rx.hstack(
        rx.cond(
            is_valid,
            rx.icon("circle-check", color=BRAND_SUCCESS, size=16),
            rx.icon("circle", color=BRAND_PRIMARY_40, size=16)
        ),
        rx.cond(
            is_valid,
            rx.text(text, color=BRAND_SUCCESS, font_size=fonts.SIZE_MICRO, font_family=fonts.FONT_FAMILY_SUPPORT),
            rx.text(text, color=BRAND_PRIMARY_40, font_size=fonts.SIZE_MICRO, font_family=fonts.FONT_FAMILY_SUPPORT)
        ),
        spacing="2",
        align="center",
        **kwargs
    )
