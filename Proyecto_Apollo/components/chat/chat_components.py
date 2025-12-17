"""Componentes de chat - Mensajes y contenedores"""

import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo.styles import chat_styles
from Proyecto_Apollo.components.header.header_components import desktop_header

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
                rx.box(
                    rx.markdown(answer, style=chat_styles.answer_style, width="100%"),
                    rx.icon_button(
                        rx.icon("copy", size=16, margin_right="4px"),
                        rx.text("Copiar respuesta", size="1"),
                        on_click=[rx.set_clipboard(answer), State.log_copy_event],
                        size="1",
                        variant="ghost",
                        color_scheme="gray",
                        margin_left="14px",
                        margin_top="-20px",
                        cursor="pointer",
                        border_radius="16px",
                    ),
                    width="98%",
                ),
            ),
        ),
        height="auto",
        margin_top="1em",
    )


def chat_container_desktop() -> rx.Component:
    """Contenedor de chat para desktop con scroll automático"""
    return rx.box(
        desktop_header(),
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
                    padding_top="6em",
                    spacing="4",
                ),
                autoscroll=State.auto_scroll_enabled,
                **chat_styles.chat_scroll_desktop_style,
            ),
            rx.center(
                rx.vstack(
                    rx.icon("message-square", size=48, color="gray"),
                    rx.text("¡Bienvenido a Apollo AI!", size="5", weight="bold"),
                    rx.text("Tu asistente experto. Pregúntame sobre:", color="gray"),
                    rx.vstack(
                        rx.text("• Productos e ingredientes activos", color="gray"),
                        rx.text("• Recomendaciones para padecimientos", color="gray"),
                        rx.text("• Plan de compensación y estrategias", color="gray"),
                        spacing="1",
                        align="center",
                    ),
                    spacing="2",
                    align="center",
                ),
                height="100%",
            ),
        ),
        width="100%",
        flex="1",
        overflow="hidden",
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
            rx.center(
                rx.vstack(
                    rx.icon("message-square", size=48, color="gray"),
                    rx.text("¡Bienvenido a Apollo AI!", size="5", weight="bold", text_align="center"),
                    rx.text("Tu asistente experto. Pregúntame sobre:", color="gray", text_align="center"),
                    rx.vstack(
                        rx.text("• Productos e ingredientes activos", color="gray", text_align="center"),
                        rx.text("• Recomendaciones para padecimientos", color="gray", text_align="center"),
                        rx.text("• Plan de compensación y estrategias", color="gray", text_align="center"),
                        spacing="1",
                        align="center",
                    ),
                    spacing="2",
                    align="center",
                    padding="2em",
                ),
                height="100%",
            ),
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
                        border_radius="14px",
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
            padding="10px",
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
    )


def mobile_chat_input() -> rx.Component:
    """Input de chat para vista mobile"""
    return rx.box(
        rx.form(
            rx.hstack(
                rx.text_area(
                    name="question",
                    value=State.question,
                    on_change=State.set_question,
                    **chat_styles.text_area_mobile_style,
                ),
                rx.icon_button(
                    rx.icon("arrow-up", size=20),
                    type="submit",
                    loading=State.is_loading,
                    **chat_styles.send_button_mobile_style,
                ),
                align="end",
                spacing="2",
                width="100%",
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
        border_radius="24px",
        padding="10px",
        margin_x="1rem",
        margin_bottom="1rem",
        box_shadow="0 4px 12px rgba(0, 0, 0, 0.1)",
        width="calc(100% - 2em)",
    )