"""Componentes de chat - Mensajes y contenedores"""

import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo.styles import chat_styles


def chat_message(question: str, answer: str) -> rx.Component:
    """Componente para mostrar un intercambio de pregunta y respuesta"""
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
                    lambda messages: chat_message(messages[0], messages[1]),
                ),
                autoscroll=State.auto_scroll_enabled,
                **chat_styles.chat_scroll_desktop_style,
            ),
            rx.text("No hay mensajes aún. ¡Escribe algo!", color="gray", padding="2em"),
        ),
    )


def chat_container_mobile() -> rx.Component:
    """Contenedor de chat para mobile que ocupa todo el espacio disponible"""
    from Proyecto_Apollo.components.layout.banner import mobile_banner
    
    return rx.box(
        rx.vstack(
            mobile_banner(),
            rx.cond(
                State.has_messages,
                rx.auto_scroll(
                    rx.foreach(
                        State.chat_history,
                        lambda messages: chat_message(messages[0], messages[1]),
                    ),
                    autoscroll=State.auto_scroll_enabled,
                    **chat_styles.chat_scroll_mobile_style,
                ),
                rx.text("No hay mensajes aún. ¡Escribe algo!", color="gray", padding="2em"),
            ),
            spacing="0",
            width="100%",
            height="100dvh",
        ),
        **chat_styles.chat_container_mobile_style,
    )


def desktop_chat_input() -> rx.Component:
    """Input de chat para vista desktop"""
    return rx.center(
        rx.form(
            rx.hstack(
                rx.text_area(
                    name="question",
                    value=State.question,
                    on_change=State.set_question,
                    **chat_styles.text_area_desktop_style,
                ),
                rx.icon_button(
                    "arrow_up",
                    type="submit",
                    loading=State.is_loading,
                    **chat_styles.send_button_desktop_style,
                ),
            ),
            on_submit=State.answer,
            width="100%",
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
            width="100%",
        ),
        width="100%",
    )
