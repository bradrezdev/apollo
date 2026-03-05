import reflex as rx
from ...styles.colors import *
from ...styles import fonts
from typing import Any

def input(placeholder: str, value: str | rx.Var[str], on_change: Any = None, type: str = "text", **kwargs) -> rx.Component:
    """Input atómico reutilizable."""
    return rx.input(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        type=type,
        height="48px",
        width="100%",
        radius="full",
        variant="soft",
        bg=rx.color_mode_cond(
            light=BRAND_BACKGROUND_ALT,
            dark=BRAND_TEXT_DARK
        ),
        color=rx.color_mode_cond(
            light=BRAND_PRIMARY_100,
            dark=BRAND_WHITE
        ),
        **kwargs
    )
