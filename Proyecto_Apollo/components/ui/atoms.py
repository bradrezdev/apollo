import reflex as rx
from ...styles.colors import *
from ...styles.fonts import FontSystem

from typing import Any

def atom_button(text: str | rx.Component, on_click: Any = None, variant: str = "primary", width="100%", **kwargs) -> rx.Component:
    """Botón atómico reutilizable que sigue el Design System."""
    
    # Base styling
    base_style = {
        "size": "4",
        "width": width,
        "border_radius": "24px",
        "font_family": FontSystem.PRIMARY_FONT,
        "font_size": FontSystem.SIZE_H3,
        "font_weight": FontSystem.WEIGHT_SEMIBOLD,
        "cursor": "pointer",
        "transition": "all 0.2s ease-in-out",
        "_hover": {"transform": "scale(1.02)"}
    }
    
    if variant == "primary":
        base_style.update({
            "bg": SECONDARY_100,
            "color": NEUTRAL_WHITE,
            "border": "none",
        })
    elif variant == "outline":
        base_style.update({
            "bg": "transparent",
            "color": NEUTRAL_WHITE,
            "border": f"2px solid {NEUTRAL_WHITE}",
        })
    elif variant == "ghost":
        base_style.update({
            "bg": "transparent",
            "color": NEUTRAL_WHITE,
            "border": "none",
            "opacity": "0.8",
            "_hover": {"opacity": "1.0", "bg": "rgba(255,255,255,0.1)"}
        })
        
    return rx.button(text, on_click=on_click, **{**base_style, **kwargs})

def atom_input(placeholder: str, value: str | rx.Var[str], on_change: Any = None, type: str = "text", **kwargs) -> rx.Component:
    """Input atómico reutilizable."""
    return rx.input(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        type=type,
        size="3",
        width="100%",
        radius="full",
        bg="rgba(255, 255, 255, 0.1)",
        color=NEUTRAL_WHITE,
        border=f"1px solid rgba(255, 255, 255, 0.2)",
        _focus={
            "border_color": SECONDARY_100,
            "box_shadow": f"0 0 0 2px {SECONDARY_100}40"
        },
        **kwargs
    )

def atom_badge(text: str, is_valid: rx.Var[bool], **kwargs) -> rx.Component:
    """Badge atómico para mostrar estados como validaciones."""
    return rx.hstack(
        rx.cond(
            is_valid,
            rx.icon("circle-check", color=SUCCESS, size=16),
            rx.icon("circle-x", color="rgba(255,255,255,0.4)", size=16)
        ),
        rx.cond(
            is_valid,
            rx.text(text, color=SUCCESS, font_size=FontSystem.SIZE_BADGE, font_family=FontSystem.SECONDARY_FONT),
            rx.text(text, color="rgba(255,255,255,0.4)", font_size=FontSystem.SIZE_BADGE, font_family=FontSystem.SECONDARY_FONT)
        ),
        spacing="2",
        align="center",
        **kwargs
    )