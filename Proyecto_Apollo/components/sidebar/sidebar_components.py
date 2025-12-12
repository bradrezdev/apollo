"""Componentes del sidebar - Navegación y conversaciones"""

import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo.styles import sidebar_styles, colors


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    """Item individual del sidebar con icono y texto"""
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style=sidebar_styles.sidebar_item_hover_style,
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_navigation() -> rx.Component:
    """Navegación principal del sidebar"""
    return rx.vstack(
        sidebar_item("Dashboard", "layout-dashboard", "/#"),
        sidebar_item("Projects", "square-library", "/#"),
        sidebar_item("Analytics", "bar-chart-4", "/#"),
        sidebar_item("Messages", "mail", "/#"),
        spacing="1",
        width="100%",
    )


def conversation_item(conversation: dict) -> rx.Component:
    """Item individual de conversación en el sidebar"""
    return rx.box(
        rx.hstack(
            rx.text(
                conversation["title"],
                size="3",
                weight="medium",
                style={
                    "overflow": "hidden",
                    "text_overflow": "ellipsis",
                    "white_space": "nowrap",
                }
            ),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            style={
                "_hover": {
                    "bg": colors.ACCENT_LIGHT,
                    "cursor": "pointer",
                },
                "border-radius": "0.5em",
            },
            on_click=lambda: State.load_conversation_and_messages(conversation["id"]),
        ),
        width="100%",
    )


def conversations_list() -> rx.Component:
    """Lista de conversaciones en el sidebar"""
    return rx.vstack(
        rx.hstack(
            rx.text("Conversaciones", size="4", weight="bold"),
            rx.spacer(),
            rx.icon_button(
                rx.icon("plus"),
                size="2",
                on_click=State.start_new_conversation,
            ),
            width="100%",
            padding_x="0.5rem",
        ),
        rx.divider(),
        rx.vstack(
            rx.foreach(
                State.conversations,
                conversation_item
            ),
            spacing="1",
            width="100%",
            max_height="300px",
            overflow_y="auto",
        ),
        spacing="2",
        width="100%",
    )


def user_profile_section() -> rx.Component:
    """Sección de perfil de usuario en el sidebar"""
    return rx.hstack(
        rx.icon_button(rx.icon("user"), size="3", radius="full"),
        rx.vstack(
            rx.box(
                rx.text(State.user_name, style=sidebar_styles.user_name_style),
                rx.text(State.user_email, style=sidebar_styles.user_email_style),
                **sidebar_styles.user_info_container_style,
            ),
        ),
    )


def desktop_sidebar() -> rx.Component:
    """Sidebar completo para vista desktop"""
    return rx.vstack(
        rx.image(**sidebar_styles.logo_style),
        rx.spacer(),
        conversations_list(),
        rx.divider(),
        sidebar_navigation(),
        rx.spacer(),
        user_profile_section(),
        **sidebar_styles.sidebar_style,
    )
