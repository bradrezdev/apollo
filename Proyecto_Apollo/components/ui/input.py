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
        padding="0 4px",
        **kwargs
    )


def password_input(
    placeholder: str,
    value: str | rx.Var[str],
    on_change: Any = None,
    show: bool | rx.Var[bool] = False,
    toggle: Any = None,
    **kwargs,
) -> rx.Component:
    """Input de contraseña con botón de visibilidad (ojo) integrado."""
    return rx.box(
        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            type=rx.cond(show, "text", "password"),
            height="48px",
            width="100%",
            radius="full",
            variant="soft",
            bg=rx.color_mode_cond(
                light=BRAND_BACKGROUND_ALT,
                dark=BRAND_TEXT_DARK,
            ),
            color=rx.color_mode_cond(
                light=BRAND_PRIMARY_100,
                dark=BRAND_WHITE,
            ),
            padding="0 32px 0 4px",
            **kwargs,
        ),
        rx.icon_button(
            rx.cond(
                show,
                rx.icon("eye-off", size=16, border_radius="32px"),
                rx.icon("eye", size=16, border_radius="32px"),
            ),
            border_radius="32px",
            on_click=toggle,
            size="1",
            variant="ghost",
            color_scheme="gray",
            position="absolute",
            right="10px",
            top="60%",
            transform="translateY(-50%)",
            cursor="pointer",
            tab_index=-1,
            aria_label="Toggle password visibility",
        ),
        position="relative",
        height="auto",
        width="100%",
    )

