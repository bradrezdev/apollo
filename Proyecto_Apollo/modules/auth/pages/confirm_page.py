import reflex as rx
from Proyecto_Apollo.modules.auth.state.confirm_state import ConfirmState


def confirm_page_ui() -> rx.Component:
    """Página de confirmación de cuenta con timer automático."""
    return rx.box(
        rx.script(
            """
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(function() {
                    window.location.href = '/';
                }, 5000);
            });
            """
        ),
        rx.center(
            rx.vstack(
                # Check animation
                rx.box(
                    rx.icon(
                        tag="check",
                        width="48px",
                        height="48px",
                        color="#0CBCE5",
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    width="80px",
                    height="80px",
                    border_radius="full",
                    background_color="rgba(12, 188, 229, 0.1)",
                    margin_bottom="24px",
                ),
                
                # Success message
                rx.heading(
                    "Tu cuenta ha sido confirmada",
                    size="2",
                    color="#062A63",
                    text_align="center",
                    margin_bottom="8px",
                ),
                
                rx.text(
                    "Ahora puedes acceder a Apollo",
                    color="#677C9A",
                    text_align="center",
                    margin_bottom="32px",
                ),
                
                # Timer
                rx.text(
                    f"Serás redirigido en {ConfirmState.countdown} segundos...",
                    color="#9AA7BB",
                    text_align="center",
                    margin_bottom="24px",
                ),
                
                # Manual button
                rx.button(
                    "Ir al login ahora",
                    on_click=ConfirmState.go_to_login,
                    background_color="#062A63",
                    color="white",
                    size="2",
                    padding="14px 32px",
                    border_radius="8px",
                    _hover={
                        "background_color": "#0d3d7a",
                    },
                ),
                
                spacing="4",
                align="center",
                max_width="400px",
                padding="40px 24px",
            ),
            width="100%",
            height="100dvh",
            background_color="#F8F9FA",
        ),
    )
