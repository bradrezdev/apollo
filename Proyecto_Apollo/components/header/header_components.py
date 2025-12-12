"""Componentes de header - Desktop y Mobile"""

import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo.styles import header_styles, colors
from Proyecto_Apollo.components.sidebar import (
    sidebar_navigation,
    sidebar_item,
    conversations_list
)


def desktop_header() -> rx.Component:
    """Header para vista desktop"""
    return rx.container(
        rx.text("TelemedicinAI", style=header_styles.title_style),
        **header_styles.header_desktop_style,
    )


def mobile_drawer_content() -> rx.Component:
    """Contenido del drawer para vista mobile"""
    return rx.vstack(
        # Botón de cerrar
        rx.box(
            rx.drawer.close(rx.icon("x", size=header_styles.icon_sizes["large"])), 
            width="100%"
        ),
        # Lista de conversaciones
        conversations_list(),
        rx.divider(),
        # Navegación principal
        sidebar_navigation(),
        rx.spacer(),
        # Sección inferior del drawer
        rx.vstack(
            rx.vstack(
                sidebar_item("Settings", "settings", "/#"),
                sidebar_item("Log out", "log-out", "/#"),
                spacing="1",
                width="100%",
            ),
            rx.divider(margin="0"),
            rx.hstack(
                rx.icon_button(rx.icon("user"), size="3", radius="full"),
                rx.vstack(
                    rx.box(
                        rx.text("My account", style=header_styles.user_name_style),
                        rx.text("user@reflex.dev", size="2", weight="medium"),
                        width="100%",
                    ),
                    spacing="0",
                    justify="start",
                    width="100%",
                ),
                padding_x="0.5rem",
                align="center",
                justify="start",
                width="100%",
            ),
            spacing="5",
            width="100%",
        ),
        spacing="5",
        width="100%",
    )


def mobile_header() -> rx.Component:
    """Header para vista mobile con drawer y diseño degradado"""
    return rx.box(
        rx.hstack(
            # Botón del drawer en box redondo
            rx.box(
                rx.drawer.root(
                    rx.drawer.trigger(
                        rx.box(
                            rx.icon("panel-right-close", **header_styles.drawer_trigger_style),
                            color=colors.WHITE,
                        )
                    ),
                    rx.drawer.overlay(z_index="5"),
                    rx.drawer.portal(
                        rx.drawer.content(
                            mobile_drawer_content(),
                            **header_styles.drawer_content_style,
                        ),
                        width="100%",
                    ),
                    direction="left",
                ),
                **header_styles.header_mobile_round_box_style,
            ),
            
            rx.spacer(),
            
            # Título en box redondeado
            rx.box(
                rx.text("TelemedicinAI", style=header_styles.mobile_title_style),
                **header_styles.header_mobile_title_box_style,
            ),
            
            rx.spacer(),
            
            # Botón de nueva conversación en box redondo
            rx.box(
                rx.icon(
                    "square-pen",
                    size=header_styles.icon_sizes["small"],
                    color=colors.WHITE,
                    on_click=State.start_new_conversation,
                ),
                **header_styles.header_mobile_round_box_style,
            ),
            
            **header_styles.header_mobile_content_style,
        ),
        **header_styles.header_mobile_gradient_style,
    )
