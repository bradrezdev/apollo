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


def conversation_item(conversation: dict) -> rx.Component:
    """Item individual de conversación en el sidebar con context menu"""
    return rx.context_menu.root(
        rx.context_menu.trigger(
            rx.box(
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
                    on_click=lambda: [
                        State.load_conversation_and_messages(conversation["id"]),
                        State.set_is_open(False)
                    ],
                ),
                width="100%",
            ),
        ),
        rx.context_menu.content(
            rx.context_menu.item(
                rx.hstack(
                    rx.icon("pencil", size=16),
                    rx.text("Editar título"),
                    spacing="2",
                ),
                on_select=lambda: State.open_edit_dialog(conversation["id"], conversation["title"]),
            ),
            rx.context_menu.separator(),
            rx.context_menu.item(
                rx.hstack(
                    rx.icon("trash-2", size=16),
                    rx.text("Eliminar"),
                    spacing="2",
                ),
                color_scheme="red",
                on_select=lambda: State.delete_conversation_confirm(conversation["id"]),
            ),
        ),
    )


def conversation_item_mobile(conversation: dict) -> rx.Component:
    """Item individual de conversación para móvil con botón de menú visible"""
    return rx.hstack(
        rx.box(
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
            flex="1",
            padding_x="0.5rem",
            padding_y="0.75rem",
            style={
                "_hover": {
                    "bg": colors.ACCENT_LIGHT,
                    "cursor": "pointer",
                },
                "border-radius": "0.5em",
            },
            on_click=lambda: [
                State.load_conversation_and_messages(conversation["id"]),
                State.set_is_open(False)
            ],
        ),
        rx.context_menu.root(
            rx.context_menu.trigger(
                rx.icon_button(
                    rx.icon("circle-ellipsis", size=18),
                    size="2",
                    variant="ghost",
                    color_scheme="gray",
                ),
            ),
            rx.context_menu.content(
                rx.context_menu.item(
                    rx.hstack(
                        rx.icon("pencil", size=16),
                        rx.text("Editar título"),
                        spacing="2",
                    ),
                    on_select=lambda: State.open_edit_dialog(conversation["id"], conversation["title"]),
                ),
                rx.context_menu.separator(),
                rx.context_menu.item(
                    rx.hstack(
                        rx.icon("trash-2", size=16),
                        rx.text("Eliminar"),
                        spacing="2",
                    ),
                    color_scheme="red",
                    on_select=lambda: State.delete_conversation_confirm(conversation["id"]),
                ),
            ),
        ),
        width="100%",
        align="center",
        spacing="2",
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


def conversations_list_mobile() -> rx.Component:
    """Lista de conversaciones en el sidebar para móvil con botones de menú visibles"""
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
                conversation_item_mobile
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


def edit_conversation_dialog() -> rx.Component:
    """Diálogo para editar el título de una conversación"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Editar título de conversación"),
            rx.dialog.description(
                "Ingresa el nuevo título para esta conversación",
                size="2",
                margin_bottom="16px",
            ),
            rx.flex(
                rx.input(
                    value=State.new_conversation_title,
                    on_change=State.set_new_conversation_title,
                    placeholder="Título de la conversación",
                    width="100%",
                ),
                spacing="3",
                margin_top="16px",
                margin_bottom="16px",
                direction="column",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        on_click=State.close_edit_dialog,
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Guardar",
                        on_click=State.save_conversation_title,
                    ),
                ),
                spacing="3",
                justify="end",
            ),
        ),
        open=State.is_edit_dialog_open,
        on_open_change=State.set_is_edit_dialog_open,
    )


def desktop_sidebar() -> rx.Component:
    """Sidebar completo para vista desktop"""
    return rx.fragment(
        rx.vstack(
            rx.image(**sidebar_styles.logo_style),
            rx.spacer(),
            conversations_list(),
            rx.spacer(),
            #user_profile_section(),
            **sidebar_styles.sidebar_style,
        ),
        edit_conversation_dialog(),
    )
