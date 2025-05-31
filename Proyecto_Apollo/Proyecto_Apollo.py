# Proyecto_Apollo.py

import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo import style


# === COMPONENTES DE CHAT ===
def chat_message(question: str, answer: str) -> rx.Component:
    """Componente para mostrar un intercambio de pregunta y respuesta"""
    return rx.box(
        rx.box(
            rx.text(question, style=style.question_style), 
            text_align="right", 
            color="white"
        ),
        rx.box(
            rx.markdown(answer, style=style.answer_style), 
            text_align="left"
        ),
        margin_y="1em",
    )


def chat_container_desktop() -> rx.Component:
    """Contenedor de chat para desktop con scroll automático"""
    return rx.box(
        rx.auto_scroll(
            rx.foreach(
                State.chat_history,
                lambda messages: chat_message(messages[0], messages[1]),
            ),
            autoscroll=State.auto_scroll_enabled,
            **style.chat_scroll_desktop_style,
        ),
    )


def chat_container_mobile() -> rx.Component:
    """Contenedor de chat para mobile que ocupa todo el espacio disponible"""
    return rx.box(
        rx.vstack(
            mobile_banner(),
            rx.auto_scroll(
                rx.foreach(
                    State.chat_history,
                    lambda messages: chat_message(messages[0], messages[1]),
                ),
                autoscroll=State.auto_scroll_enabled,
                **style.chat_scroll_mobile_style,
            ),
            spacing="0",
            width="100%",
            height="100%",
        ),
        **style.chat_container_mobile_style,
    )


# === COMPONENTES DE SIDEBAR ===
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
            style=style.sidebar_item_hover_style,
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


def user_profile_section() -> rx.Component:
    """Sección de perfil de usuario en el sidebar"""
    return rx.hstack(
        rx.icon_button(rx.icon("user"), size="3", radius="full"),
        rx.vstack(
            rx.box(
                rx.text(State.user_name, style=style.user_name_style),
                rx.text(State.user_email, style=style.user_email_style),
                **style.user_info_container_style,
            ),
        ),
    )


def desktop_sidebar() -> rx.Component:
    """Sidebar completo para vista desktop"""
    return rx.vstack(
        rx.image(**style.logo_style),
        rx.spacer(),
        sidebar_navigation(),
        rx.spacer(),
        user_profile_section(),
        **style.sidebar_style,
    )


# === COMPONENTES DE HEADER ===
def desktop_header() -> rx.Component:
    """Header para vista desktop"""
    return rx.container(
        rx.text("TelemedicinAI", style=style.title_style),
        **style.header_desktop_style,
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
                            rx.icon("panel-right-close", **style.drawer_trigger_style),
                            color=style.WHITE,
                        )
                    ),
                    rx.drawer.overlay(z_index="5"),
                    rx.drawer.portal(
                        rx.drawer.content(
                            mobile_drawer_content(),
                            **style.drawer_content_style,
                        ),
                        width="100%",
                    ),
                    direction="left",
                ),
                **style.header_mobile_round_box_style,
            ),
            
            rx.spacer(),
            
            # Título en box redondeado
            rx.box(
                rx.text("TelemedicinAI", style=style.mobile_title_style),
                **style.header_mobile_title_box_style,
            ),
            
            rx.spacer(),
            
            # Ícono square-pen en box redondo
            rx.box(
                rx.icon("square-pen", size=style.icon_sizes["small"], color=style.WHITE),
                **style.header_mobile_round_box_style,
            ),
            
            **style.header_mobile_content_style,
        ),
        **style.header_mobile_gradient_style,
    )


def mobile_drawer_content() -> rx.Component:
    """Contenido del drawer para vista mobile"""
    return rx.vstack(
        # Botón de cerrar
        rx.box(
            rx.drawer.close(rx.icon("x", size=style.icon_sizes["large"])), 
            width="100%"
        ),
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
                        rx.text("My account", style=style.user_name_style),
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


# === COMPONENTES DE INPUT ===
def desktop_chat_input() -> rx.Component:
    """Input de chat para vista desktop"""
    return rx.center(
        rx.hstack(
            rx.text_area(
                value=State.question,
                on_change=State.set_question,
                **style.text_area_desktop_style,
            ),
            rx.icon_button(
                "arrow_up",
                on_click=State.answer,
                **style.send_button_desktop_style,
            ),
        ),
        width="100%",
    )


def mobile_chat_input() -> rx.Component:
    """Input de chat para vista mobile"""
    return rx.box(
        rx.flex(
            rx.text_area(
                value=State.question,
                on_change=State.set_question,
                **style.text_area_mobile_style,
            ),
            rx.icon_button(
                "arrow-up",
                on_click=State.answer,
                **style.send_button_mobile_style,
            ),
            **style.chat_input_style,
        ),
        width="100%",
    )


# === COMPONENTES DE BANNER ===
def desktop_banner() -> rx.Component:
    """Banner para vista desktop"""
    return rx.box(
        rx.image(
            src="/banner_web.jpg",
            **style.banner_desktop_style,
        ),
        **style.banner_container_desktop_style,
    )


def mobile_banner() -> rx.Component:
    """Banner para vista mobile"""
    return rx.container(
        rx.image(
            src="/banner_web.jpg",
            **style.banner_mobile_style,
        ),
        **style.banner_container_mobile_style,
    )


# === LAYOUTS PRINCIPALES ===
def desktop_layout() -> rx.Component:
    """Layout completo para vista desktop"""
    return rx.hstack(
        # Sidebar
        desktop_sidebar(),
        # Área de chat
        rx.vstack(
            desktop_header(),
            rx.flex(
                rx.vstack(
                    desktop_banner(),
                    chat_container_desktop(),
                ),
                **style.desktop_layout_style,
            ),
            desktop_chat_input(),
            **style.chat_container_desktop_style,
        ),
    )


def mobile_layout() -> rx.Component:
    """Layout completo para vista mobile"""
    return rx.box(
        # Header fijo
        mobile_header(),
        # Contenedor principal del chat
        chat_container_mobile(),
        # Input fijo
        mobile_chat_input(),
        **style.mobile_chat_main_container_style,
    )


# === COMPONENTE PRINCIPAL ===
def index() -> rx.Component:
    """Página principal de la aplicación"""
    return rx.hstack(
        # Vista para desktop y tablet
        rx.tablet_and_desktop(desktop_layout()),
        # Vista para mobile
        rx.mobile_only(mobile_layout()),
        **style.main_container_style,
    )


# === CONFIGURACIÓN DE LA APP ===
app = rx.App(
    theme=rx.theme(
        accent_color="yellow",
        appearance="inherit",
        has_background=True,
        radius="large",
    )
)

app.add_page(index)