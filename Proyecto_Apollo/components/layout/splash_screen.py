"""Componente Splash Screen - Se muestra solo en PWA/Standalone mientras carga"""

import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo.styles.colors import ApolloTheme

def splash_screen() -> rx.Component:
    """
    Pantalla de carga inicial que solo se muestra en modo standalone (PWA)
    y desaparece cuando la carga inicial de datos ha terminado.
    """
    return rx.cond(
        State.is_initial_load,
        rx.center(
            rx.vstack(
                # Aquí irá el logo de la App en el futuro
                rx.image(src="/logotipo-onano.svg", width="80%"),
                rx.spinner(size="3", color=ApolloTheme.light_colors()["primary"]),
                spacing="4",
                align="center",
            ),
            background_color=rx.color_mode_cond(
                light=ApolloTheme.light_colors()["background_color"],
                dark=ApolloTheme.dark_colors()["background_color"]
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            z_index="9999",
            # Lógica CSS para mostrar SOLO si es standalone (PWA)
            # Por defecto display: none, y si cumple la media query lo cambiamos a flex
            display="none",
            style={
                "@media (display-mode: standalone)": {
                    "display": "flex"
                },
                # Compatibilidad iOS
                "@media (display-mode: fullscreen)": {
                    "display": "flex"
                },
                "@media (display-mode: minimal-ui)": {
                    "display": "flex"
                }
            }
        ),
        rx.fragment() # Retornar fragmento vacío si no es carga inicial
    )
