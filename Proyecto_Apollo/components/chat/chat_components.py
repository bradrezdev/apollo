"""Componentes de chat - Mensajes y contenedores"""

import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo.styles import chat_styles

# Import de colores personalizados
from ...styles.colors import ApolloTheme


def chat_message(qa: tuple[str, str]) -> rx.Component:
    """
    Componente para mostrar un intercambio de pregunta y respuesta
    
    Args:
        qa: Tupla con (pregunta, respuesta)
    
    Returns:
        rx.Component: Box con el mensaje del usuario y la respuesta del asistente
    """
    question, answer = qa[0], qa[1]
    
    return rx.box(
        rx.box(
            rx.text(question, style=chat_styles.question_style), 
            text_align="right", 
            color="white"
        ),
        rx.box(
            rx.cond(
                answer == "",
                # Mostrar indicador de "pensando" cuando la respuesta está vacía
                rx.hstack(
                    rx.spinner(size="2"),
                    rx.text("Pensando en su respuesta...", color="gray", font_size="0.9em"),
                    spacing="2",
                ),
                # Mostrar respuesta completa con botón de copiar
                rx.hstack(
                    rx.markdown(answer, style=chat_styles.answer_style),
                    rx.icon_button(
                        rx.icon("copy", size=16),
                        on_click=rx.set_clipboard(answer),
                        size="1",
                        variant="ghost",
                        color_scheme="gray",
                    ),
                    align="start",
                    width="100%",
                ),
            ),
            text_align="left"
        ),
        margin_y="1em",
    )


def chat_container_desktop() -> rx.Component:
    """Contenedor de chat para desktop con scroll automático"""
    return rx.box(
        rx.cond(
            State.has_messages,
            rx.auto_scroll(
                rx.vstack(
                    rx.foreach(
                        State.chat_history,
                        chat_message,
                    ),
                    width="100%",
                    max_width="900px",
                    margin_x="auto",
                    padding_bottom="4rem",
                    spacing="4",
                ),
                autoscroll=State.auto_scroll_enabled,
                **chat_styles.chat_scroll_desktop_style,
            ),
            rx.center(
                rx.vstack(
                    rx.icon("message-square", size=48, color="gray"),
                    rx.text("¡Bienvenido a Apollo AI!", size="5", weight="bold"),
                    rx.text("Escribe un mensaje para comenzar una conversación.", color="gray"),
                    spacing="4",
                    align="center",
                ),
                height="100%",
            ),
        ),
        width="100%",
        height="100%",
        padding_top="2rem",
    )


def chat_container_mobile() -> rx.Component:
    """Contenedor de chat para mobile que ocupa todo el espacio disponible"""
    
    return rx.box(
        rx.cond(
            State.has_messages,
            rx.auto_scroll(
                rx.foreach(
                    State.chat_history,
                    chat_message,
                ),
                autoscroll=State.auto_scroll_enabled,
                **chat_styles.chat_scroll_mobile_style,
            ),
            rx.text("No hay mensajes aún. ¡Escribe algo!", color="gray", padding="2em"),
        ),
        **chat_styles.chat_container_mobile_style,
    )


def desktop_chat_input() -> rx.Component:
    """Input de chat para vista desktop"""
    return rx.center(
        rx.box(
            rx.form(
                rx.hstack(
                    rx.text_area(
                        name="question",
                        value=State.question,
                        on_change=State.set_question,
                        **chat_styles.text_area_desktop_style,
                    ),
                    rx.icon_button(
                        rx.icon("arrow-up", size=20),
                        type="submit",
                        loading=State.is_loading,
                        **chat_styles.send_button_desktop_style,
                    ),
                    align="end",
                    spacing="3",
                ),
                on_submit=State.answer,
                reset_on_submit=True,
                width="100%",
            ),
            bg=rx.color_mode_cond(
                light=ApolloTheme.light_colors()["input_background"],
                dark=ApolloTheme.dark_colors()["input_background"]
            ),
            style={
                "backdropFilter": "blur(20px)",
                "-webkit-backdrop-filter": "blur(20px)",
            },
            border=rx.color_mode_cond(
                light=f"1px solid {ApolloTheme.light_colors()['input_border']}",
                dark="1px solid rgba(255, 255, 255, 0.1)",
            ),
            border_radius="24px",
            padding="1rem",
            box_shadow=rx.color_mode_cond(
                light=ApolloTheme.light_colors()["box_shadow"],
                dark="0 4px 20px rgba(0, 0, 0, 0.4)",
            ),
            width="60%",
            min_width="600px",
            margin_bottom="2rem",
            transition="all 0.2s ease-in-out",
            _hover={
                "box_shadow": rx.color_mode_cond(
                    light=ApolloTheme.light_colors()["box_shadow_hover"],
                    dark="0 8px 30px rgba(0, 0, 0, 0.5)",
                ),
            },
        ),
        width="100%",
        padding_bottom="1rem",
    )


def mobile_chat_input() -> rx.Component:
    """Input de chat para vista mobile"""
    return rx.box(
        rx.form(
            rx.flex(
                rx.input(
                    name="question",
                    border_radius="40px",
                    padding="4px",
                    height="3em",
                    font_size="1em",
                    bg=rx.color_mode_cond(
                        light="rgba(25, 25, 25, 0.15)",
                        dark=ApolloTheme.dark_colors()["input_background"]
                    ),
                    value=State.question,
                    on_change=State.set_question,
                    **chat_styles.text_area_mobile_style,
                ),
                rx.icon_button(
                    "arrow-up",
                    type="submit",
                    loading=State.is_loading,
                    **chat_styles.send_button_mobile_style,
                ),
                **chat_styles.chat_input_style,
            ),
            on_submit=State.answer,
            reset_on_submit=True,
            width="90%",
            margin_left="auto",
            margin_right="auto",
            margin_bottom="1rem",
        ),
        width="100%",
    )