"""Componentes de chat - Mensajes y contenedores"""

import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo.styles import chat_styles
from Proyecto_Apollo.components.header.header_components import desktop_header, mobile_header

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









def responsive_chat_input() -> rx.Component:
    """Input de chat unificado y responsivo"""
    return rx.center(
        rx.box(
            rx.form(
                rx.hstack(
                    rx.text_area(
                        name="question",
                        value=State.question,
                        on_change=State.set_question,
                        placeholder="Escribe tu mensaje aquí...",
                        bg="transparent",
                        color=rx.color_mode_cond(light="black", dark="white"),
                        border="none",
                        _focus={"outline": "none"},
                        width="100%",
                        auto_height=True,
                        max_height="150px",
                        rows="1",
                        resize="none",
                        padding_y="8px",
                        style={"font_family": "Poppins", "font_size": "16px"},
                    ),
                    rx.icon_button(
                        rx.icon("arrow-up", size=20),
                        type="submit",
                        loading=State.is_loading,
                        variant="solid",
                        color_scheme="blue",
                        border_radius="50%",
                        size="3",
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
            box_shadow=rx.color_mode_cond(
                light=ApolloTheme.light_colors()["box_shadow"],
                dark="0 4px 20px rgba(0, 0, 0, 0.4)",
            ),
            width=["92%", "92%", "60%", "60%"],
            min_width=["0", "0", "600px", "600px"],
            position="fixed",
            bottom=["1rem", "1rem", "2rem", "2rem"],
            z_index="1000",
            transition="all 0.2s ease-in-out",
            _hover={
                "box_shadow": rx.color_mode_cond(
                    light=ApolloTheme.light_colors()["box_shadow_hover"],
                    dark="0 8px 30px rgba(0, 0, 0, 0.5)",
                ),
            },
        ),
        width="100%",
        position="absolute",
        bottom="0",
        z_index="900",
        padding_bottom=["0", "0", "2rem", "2rem"],
        pointer_events="none", 
    )


def responsive_chat_container() -> rx.Component:
    """Contenedor de chat unificado para todas las vistas"""
    return rx.box(
        rx.box(mobile_header(), display=["block", "block", "none", "none"]),
        rx.box(desktop_header(), display=["none", "none", "block", "block"]),
        
        rx.cond(
            State.has_messages,
            rx.auto_scroll(
                rx.vstack(
                    rx.foreach(
                        State.chat_history,
                        chat_message,
                    ),
                    width=["94%", "94%", "100%", "100%"],
                    max_width="900px",
                    margin_x="auto",
                    padding_top=["5em", "5em", "6em", "6em"],
                    padding_bottom=["150px", "150px", "150px", "150px"],
                    spacing="4",
                ),
                autoscroll=State.auto_scroll_enabled,
                style={
                    "height": "100vh",
                    "overflow_y": "auto",
                    "scroll_behavior": "smooth",
                    "&::-webkit-scrollbar": {"display": "none"},
                    "-ms-overflow-style": "none",
                    "scrollbar-width": "none",
                }
            ),
            rx.center(
                rx.vstack(
                    rx.icon("message-square", size=48, color="#0CBCE5"),
                    rx.text("¡Bienvenido a Apollo AI!", size="6", weight="bold", color="#062A63"),
                    rx.text("Tu asistente experto en ONANO.", color="gray"),
                    rx.divider(width="50%"),
                    rx.vstack(
                        rx.hstack(rx.icon("sparkles", size=16, color="#0CBCE5"), rx.text("Productos y Nanotecnología", color="gray")),
                        rx.hstack(rx.icon("trending-up", size=16, color="#0CBCE5"), rx.text("Plan de Compensación", color="gray")),
                        rx.hstack(rx.icon("activity", size=16, color="#0CBCE5"), rx.text("Salud y Bienestar", color="gray")),
                        spacing="2",
                        align="start",
                    ),
                    spacing="4",
                    align="center",
                ),
                height="100vh",
                width="100%",
                padding_bottom="100px",
            ),
        ),
        
        responsive_chat_input(),
        
        width="100%",
        height="100vh",
        position="relative",
    )
