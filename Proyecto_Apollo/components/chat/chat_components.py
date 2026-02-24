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
    """Input de chat unificado y responsivo — Mobile First"""
    return rx.box(
        rx.form(
            rx.hstack(
                rx.el.textarea(
                    name="question",
                    value=State.question,
                    on_change=State.set_question,
                    placeholder="Escribe tu mensaje aquí...",
                    rows=1,
                    style={
                        "width": "100%",
                        "min_height": "40px",
                        "max_height": "132px",  # ~5 líneas
                        "resize": "none",
                        "overflow_y": "auto",
                        "border": "none",
                        "outline": "none",
                        "background": "transparent",
                        "font_family": "Poppins, sans-serif",
                        "font_size": "16px",
                        "padding": "8px 12px",
                        "line_height": "1.5",
                        "field_sizing": "content",
                        "color": rx.color_mode_cond(light="#383A3F", dark="#FFFFFF"),
                    },
                ),
                rx.icon_button(
                    rx.icon("arrow-up", size=20),
                    type="submit",
                    loading=State.is_loading,
                    variant="solid",
                    bg="#0CBCE5",
                    color="white",
                    _hover={"bg": "#3DC9EA"},
                    border_radius="50%",
                    size="3",
                    cursor="pointer",
                    flex_shrink="0",
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
            light="rgba(255, 255, 255, 0.85)",
            dark="rgba(30, 30, 35, 0.85)",
        ),
        backdrop_filter="blur(20px)",
        border=rx.color_mode_cond(
            light="1px solid rgba(6, 42, 99, 0.1)",
            dark="1px solid rgba(255, 255, 255, 0.1)",
        ),
        border_radius="24px",
        padding="8px 12px",
        box_shadow=rx.color_mode_cond(
            light="0 4px 24px rgba(6, 42, 99, 0.10)",
            dark="0 4px 20px rgba(0, 0, 0, 0.4)",
        ),
        # Responsivo: ancho
        width=["92%", "92%", "min(60%, 800px)", "min(60%, 800px)"],
        # Posicionamiento fijo centrado
        position="fixed",
        bottom=["0.75rem", "0.75rem", "1.5rem", "1.5rem"],
        left="50%",
        transform=["translateX(-50%)", "translateX(-50%)", "translateX(calc(-50% + 150px))", "translateX(calc(-50% + 150px))"],
        z_index="1000",
        transition="box-shadow 0.2s ease",
        _hover={
            "box_shadow": rx.color_mode_cond(
                light="0 8px 32px rgba(6, 42, 99, 0.15)",
                dark="0 8px 30px rgba(0, 0, 0, 0.5)",
            ),
        },
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
