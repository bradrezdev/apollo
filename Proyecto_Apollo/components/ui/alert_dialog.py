import reflex as rx

from typing import Any
from .button import button

# Import de fuentes y colores para usar en el dialog
from ...styles.colors import *
from ...styles.fonts import *

def dialog(title: str, description: str, on_confirm: Any = None, on_cancel: Any = None, **kwargs) -> rx.Component:
    """Dialog de alerta atómico."""
    return rx.dialog.root(
        rx.dialog.trigger(
            button("Abrir Dialog", variant="outline", width="auto")
        ),
        rx.dialog.content(
            rx.vstack(
                rx.dialog.title(
                    title,
                    style=STYLE_H2,
                    margin_bottom="-8px",
                ),
                rx.dialog.description(
                    description,
                    style=STYLE_BODY,
                ),
                padding="12px 20px 20px 20px",
                width="100%",
            ),
            rx.dialog.close(
                button(
                    "OK", 
                    variant="primary",
                    on_click=on_cancel,
                    width="100%",
                )
            ),
            width="90%",
            max_width="360px",
            padding="18px",
            border_radius="32px",
            bg=rx.color_mode_cond(
                light=f"{BRAND_WHITE}DD",
                dark=f"{BRAND_TEXT_DARK}"
            ),
            backdrop_filter="blur(8px)",
        ),
        **kwargs
    )

def alert_dialog(title: str, description: str, on_confirm: Any = None, on_cancel: Any = None, **kwargs) -> rx.Component:
    """Dialog de alerta atómico."""
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            button("Abrir Alerta", variant="outline", width="auto")
        ),
        rx.alert_dialog.content(
            rx.vstack(
                rx.alert_dialog.title(
                    title,
                    style=STYLE_H2,
                    margin_bottom="-8px",
                ),
                rx.alert_dialog.description(
                    description,
                    style=STYLE_BODY,
                ),
                padding="12px 20px 20px 20px",
                width="100%",
            ),
            rx.hstack(
                rx.alert_dialog.cancel(
                    button(
                        "Cancel", 
                        variant="ghost",
                        on_click=on_cancel,
                        width="50%",
                    )
                ),
                rx.alert_dialog.action(
                    button(
                        "OK", 
                        variant="primary",
                        on_click=on_confirm,
                        width="50%",
                    )
                ),
                spacing="2",
            ),
            width="90%",
            max_width="360px",
            padding="18px",
            border_radius="32px",
            bg=rx.color_mode_cond(
                light=f"{BRAND_WHITE}DD",
                dark=f"{BRAND_TEXT_DARK}"
            ),
            backdrop_filter="blur(8px)",
        ),
        **kwargs
    )