"""Componentes de header - Desktop y Mobile"""

import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo.styles import header_styles, colors
from Proyecto_Apollo.components.sidebar import (
    sidebar_item,
    conversations_list_mobile
)

# Importar colores
from ...styles.colors import ApolloTheme


def desktop_header() -> rx.Component:
    """Header para vista desktop"""
    return rx.box(
        rx.flex(
            rx.text(
                rx.cond(
                    State.current_conversation_title != "",
                    "Apollo AI - " + State.current_conversation_title,
                    "Apollo AI"
                ),
                **header_styles.header_text_style,
            ),
            **header_styles.header_desktop_style,
        ),
        position="relative",
        width="100%",
        z_index="100",
    )


def mobile_drawer_content() -> rx.Component:
    """Contenido del drawer para vista mobile"""
    return rx.vstack(
        # Botón de cerrar
        rx.box(
            rx.drawer.close(
                rx.icon(
                    "x",
                    size=header_styles.icon_sizes["large"],
                    )
                ), 
            width="100%"
        ),
        # Lista de conversaciones para móvil con botones visibles
        conversations_list_mobile(),
        rx.divider(),
        rx.spacer(),
        # Sección inferior del drawer
        # rx.vstack(
        #     rx.vstack(
        #         sidebar_item("Settings", "settings", "/#"),
        #         sidebar_item("Log out", "log-out", "/#"),
        #         spacing="1",
        #         width="100%",
        #     ),
        #     rx.divider(margin="0"),
        #     rx.hstack(
        #         rx.icon_button(rx.icon("user"), size="3", radius="full"),
        #         rx.vstack(
        #             rx.box(
        #                 rx.text("My account", style=header_styles.user_name_style),
        #                 rx.text("user@reflex.dev", size="2", weight="medium"),
        #                 width="100%",
        #             ),
        #             spacing="0",
        #             justify="start",
        #             width="100%",
        #         ),
        #         padding_x="0.5rem",
        #         align="center",
        #         justify="start",
        #         width="100%",
        #     ),
        #     spacing="5",
        #     width="100%",
        # ),
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
                            style=header_styles.mobile_title_style,
                        )
                    ),
                    rx.drawer.overlay(z_index="5"),
                    rx.drawer.portal(
                        rx.drawer.content(
                            mobile_drawer_content(),
                            **header_styles.drawer_content_style,
                        ),
                    ),
                    direction="left",
                    open=State.is_open,
                    on_open_change=State.set_is_open,
                ),
                **header_styles.header_mobile_round_box_style,
            ),
            
            rx.spacer(),
            
            # Título en box redondeado
            rx.box(
                rx.text("Apollo AI", style=header_styles.mobile_title_style),
                **header_styles.header_mobile_title_box_style,
            ),
            
            rx.spacer(),
            
            # Botón de nueva conversación en box redondo
            rx.box(
                rx.icon(
                    "message-circle-plus",
                    size=header_styles.icon_sizes["small"],
                    style=header_styles.mobile_title_style,
                    on_click=State.start_new_conversation,
                ),
                **header_styles.header_mobile_round_box_style,
            ),
            
            **header_styles.header_mobile_content_style,
        ),
        **header_styles.header_mobile_gradient_style,
    )
