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
            rx.markdown(answer, style=chat_styles.answer_style), 
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
                rx.foreach(
                    State.chat_history,
                    chat_message,  # Usar función nombrada en lugar de lambda
                ),
                autoscroll=State.auto_scroll_enabled,
                **chat_styles.chat_scroll_desktop_style,
            ),
            rx.text("No hay mensajes aún. ¡Escribe algo!", color="gray", padding="2em"),
        ),
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
                        "arrow-up",
                        type="submit",
                        loading=State.is_loading,
                        **chat_styles.send_button_desktop_style,
                    ),
                ),
                on_submit=State.answer,
                reset_on_submit=True,
                width="100%",
            ),
            bg="rgba(255, 255, 255, 0.35)",
            style={
                "backdropFilter": "blur(60px)",
                "-webkit-backdrop-filter": "blur(60px)",
            },
            border_radius="40px",
            padding="1rem",
            box_shadow="0 4px 12px rgba(0, 0, 0, 0.1)",
            width="95%",
            margin_bottom="1rem",
        ),
        width="100%",
    )


def mobile_chat_input() -> rx.Component:
    """Input de chat para vista mobile"""
    return rx.box(
        rx.form(
            rx.flex(
                rx.input(
                    name="question",
                    variant="soft",
                    border_radius="40px",
                    size="3",
                    bg=rx.color_mode_cond(
                        light=ApolloTheme.light_colors()["input_background"],
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
            width="95%",
            margin_left="auto",
            margin_right="auto",
            margin_bottom="1rem",
        ),
        width="100%",
    )