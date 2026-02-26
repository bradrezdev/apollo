import reflex as rx
from typing import Any
from .button import atom_button

def atom_alert_dialog(title: str, description: str, on_confirm: Any = None, on_cancel: Any = None, **kwargs) -> rx.Component:
    """Dialog de alerta atómico."""
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            atom_button("Abrir Alerta", variant="outline", width="auto")
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title(title),
            rx.alert_dialog.description(description),
            rx.flex(
                rx.alert_dialog.cancel(
                    atom_button("Cancelar", variant="ghost", on_click=on_cancel, width="auto")
                ),
                rx.alert_dialog.action(
                    atom_button("Confirmar", variant="primary", on_click=on_confirm, width="auto")
                ),
                spacing="3",
                justify="end",
                margin_top="16px"
            ),
        ),
        **kwargs
    )
