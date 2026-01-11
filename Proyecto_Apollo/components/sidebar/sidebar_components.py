"""Componentes del sidebar - Navegación y conversaciones"""

import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo.styles import sidebar_styles, header_styles, colors

# Import de colores personalizados
from ...styles.colors import ApolloTheme


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
                    padding="0.5em",
                    style={
                        "_hover": {
                            "bg": rx.color_mode_cond(
                                light=ApolloTheme.light_colors()["sidebar_item_hover"],
                                dark=ApolloTheme.dark_colors()["sidebar_item_hover"]
                            ),
                            "cursor": "pointer",
                        },
                        "border-radius": "16px",
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
                        align="center",
                        spacing="2",
                    ),
                    border_radius="18px",
                    on_select=lambda: [State.set_should_reopen_drawer(False), State.open_edit_dialog(conversation["id"], conversation["title"])],
                ),
                rx.context_menu.separator(),
                rx.context_menu.item(
                    rx.hstack(
                        rx.icon("trash-2", size=16),
                        rx.text("Eliminar"),
                        align="center",
                        spacing="2",
                    ),
                    border_radius="18px",
                    color_scheme="red",
                    on_select=lambda: [State.set_should_reopen_drawer(False), State.open_delete_dialog(conversation["id"])],
                ),
            border_radius="20px",
        ),
        on_open_change=State.log_context_menu_open,
    )


def conversation_item_mobile(conversation: dict) -> rx.Component:
    """Item individual de conversación para móvil con botón de menú visible"""
    return rx.hstack(
        rx.box(
            rx.text(
                conversation["title"],
                size="3",
                style={
                    "overflow": "hidden",
                    "text_overflow": "ellipsis",
                    "white_space": "nowrap",
                    "color": rx.color_mode_cond(
                        light=ApolloTheme.light_colors()["header_text_color"],
                        dark=ApolloTheme.dark_colors()["header_text_color"]
                    ),
                },
            ),
            flex="1",
            min_width="0",
            padding_x="0.5rem",
            padding_y="0.5rem",
            style={
                "_hover": {
                    "bg": rx.color_mode_cond(
                        light=ApolloTheme.light_colors()["sidebar_item_hover"],
                        dark=ApolloTheme.dark_colors()["sidebar_item_hover"]
                    ),
                    "cursor": "pointer",
                },
                "border-radius": "0.5em",
            },
            on_click=lambda: [
                State.load_conversation_and_messages(conversation["id"]),
                State.set_is_open(False)
            ],
        ),
        rx.menu.root(
            rx.menu.trigger(
                rx.icon_button(
                    rx.icon("circle-ellipsis", size=18),
                    size="2",
                    variant="ghost",
                    color_scheme="gray",
                ),
            ),
            rx.menu.content(
                rx.menu.item(
                    rx.hstack(
                        rx.icon("pencil", size=16),
                        rx.text("Editar título"),
                        align="center",
                        spacing="2",
                    ),
                    border_radius="18px",
                    on_select=lambda: [State.set_should_reopen_drawer(True), State.set_is_open(False), State.open_edit_dialog(conversation["id"], conversation["title"])],
                ),
                rx.menu.separator(),
                rx.menu.item(
                    rx.hstack(
                        rx.icon("trash-2", size=16),
                        rx.text("Eliminar"),
                        align="center",
                        spacing="2",
                    ),
                    border_radius="18px",
                    color_scheme="red",
                    on_select=lambda: [State.set_should_reopen_drawer(True), State.set_is_open(False), State.open_delete_dialog(conversation["id"])],
                ),
                border_radius="20px",
                z_index="50",
            ),
            on_open_change=State.log_context_menu_open,
        ),
        width="270px",
        align="center",
        spacing="2",
    )


def conversations_list() -> rx.Component:
    """Lista de conversaciones en el sidebar"""
    return rx.vstack(
        rx.button(
            rx.icon("plus", size=18),
            "Nuevo chat",
            border_radius="32px",
            padding_y="20px",
            cursor="pointer",
            margin_bottom="2em",
            on_click=State.start_new_conversation,
            variant="surface",
            width="100%",
        ),
        rx.divider(),
        rx.text("Conversaciones", size="2", weight="bold", color="gray", padding_left="0.5rem"),
        rx.vstack(
            rx.cond(
                State.is_loading_conversations,
                rx.vstack(
                    rx.skeleton(height="40px", width="100%"),
                    rx.skeleton(height="40px", width="100%"),
                    rx.skeleton(height="40px", width="100%"),
                    spacing="2",
                    width="100%"
                ),
                rx.vstack(
                    rx.foreach(
                        State.conversations,
                        conversation_item
                    ),
                    spacing="1",
                    width="100%",
                )
            ),
            width="100%",
            max_height="calc(87dvh - 200px)",
            overflow_y="auto",
            padding_right="0.5rem",
        ),
        spacing="3",
        width="100%",
    )


def conversations_list_mobile() -> rx.Component:
    """Lista de conversaciones en el sidebar para móvil con botones de menú visibles"""
    return rx.vstack(
        rx.hstack(
            rx.text("Conversaciones", size="4", weight="bold"),
            rx.spacer(),
            rx.box(
                rx.icon(
                    "message-circle-plus",
                    size=header_styles.icon_sizes["small"],
                    on_click=State.start_new_conversation,
                ),
                **header_styles.header_mobile_round_box_style,
            ),
            width="100%",
            padding_x="0.5rem",
            align="center",
        ),
        rx.divider(),
        rx.vstack(
            rx.foreach(
                State.conversations,
                conversation_item_mobile
            ),
            spacing="1",
            width="290px",
            max_height="76dvh",
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
                    border_radius="32px",
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
                        border_radius="32px",
                        padding_x="32px",
                        variant="soft",
                        color_scheme="gray",
                        on_click=lambda: [State.close_edit_dialog(), State.reopen_drawer_if_needed()],
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Guardar",
                        border_radius="32px",
                        padding_x="32px",
                        on_click=lambda: [State.save_conversation_title(), State.reopen_drawer_if_needed()],
                    ),
                ),
                spacing="3",
                justify="center",
            ),
            border_radius="30px",
            z_index="10000",
        ),
        open=State.is_edit_dialog_open,
        on_open_change=State.set_is_edit_dialog_open,
    )


def delete_conversation_dialog() -> rx.Component:
    """Diálogo para confirmar la eliminación de una conversación"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("¿Eliminar conversación?"),
            rx.dialog.description(
                "Esta acción no se puede deshacer. ¿Estás seguro de que quieres eliminar esta conversación?",
                size="2",
                margin_bottom="16px",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        border_radius="32px",
                        padding_x="32px",
                        variant="soft",
                        color_scheme="gray",
                        on_click=lambda: [State.close_delete_dialog(), State.reopen_drawer_if_needed()],
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Eliminar",
                        border_radius="32px",
                        padding_x="32px",
                        color_scheme="red",
                        on_click=lambda: [State.confirm_delete_conversation(), State.reopen_drawer_if_needed()],
                    ),
                ),
                spacing="3",
                justify="center",
                margin_top="16px",
            ),
            border_radius="30px",
            z_index="10000",
        ),
        open=State.is_delete_dialog_open,
        on_open_change=State.set_is_delete_dialog_open,
    )


def desktop_sidebar() -> rx.Component:
    """Sidebar completo para vista desktop"""
    return rx.fragment(
        rx.vstack(
            rx.image(**sidebar_styles.logo_style),
            conversations_list(),
            #user_profile_section(),
            **sidebar_styles.sidebar_style,
        ),
    )