import reflex as rx
from Proyecto_Apollo.state import State
from Proyecto_Apollo import style

def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=style.question_style),
            text_align="right",
        ),
        rx.box(
            rx.text(answer, style=style.answer_style),
            text_align="left",
        ),
        margin_y="1em",
    )

def chat() -> rx.Component:
    return rx.box(
        rx.auto_scroll(
            rx.foreach(
                State.chat_history,
                lambda messages: qa(messages[0], messages[1]),
            ),
            scroll_behavior="smooth",
            autoscroll=True,
            height="100%",
            width="100%",
        ),
    )

def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=State.question,
            placeholder="Ask a question",
            on_change=State.set_question,
            style=style.input_style,
        ),
        rx.button(
            "Ask",
            on_click=State.answer,
            style=style.button_style,
        ),
    )

def sidebar_item(
    text: str, icon: str, href: str
) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Dashboard", "layout-dashboard", "/#"),
        sidebar_item("Projects", "square-library", "/#"),
        sidebar_item("Analytics", "bar-chart-4", "/#"),
        sidebar_item("Messages", "mail", "/#"),
        spacing="1",
        width="100%",
    )

def index():
    return rx.hstack(
        # Sidebar menu.
        rx.tablet_and_desktop(
            rx.vstack(
                rx.image(src="/logoNNprotect.png"),
                rx.spacer(),
                sidebar_items(),
                rx.spacer(),
                rx.hstack(
                    rx.icon_button(
                        rx.icon("user"),
                        size="3",
                        radius="full",
                    ),
                    rx.vstack(
                        rx.box(
                            rx.text(
                                "Mi cuenta",
                                size="3",
                                weight="bold",
                            ),
                            rx.text(
                                "b.nunez@hotmail.es",
                                size="1",
                                weight="medium",
                            ),
                            width="100%",
                        ),
                    ),
                ),
                bg="white",
                padding="1rem",
                height="100vh",
                width="220px",
            ),
        ),
        # Sección de chat.
        rx.vstack(
            # Header TelemedicinAI.
            rx.container(
                "TelemedicinAI",
                bg="gold",
                height="8vh",
                margin_bottom="1vh",
                width="100%",
            ),
            # Imagen banner NN Protect.
            rx.container(
                "Imagen banner NN Protect",
                bg="orange",
                height="16vh",
                width="100%",
            ),
            # Sección de chat.
            rx.flex(
                chat(),
                height="62vh",
                overflow_y="auto",
                width="100%",
            ),
            # Sección de pregunta al chat.
            rx.hstack(
                rx.form(
                    # Input de pregunta al asistente.
                    rx.input(
                        value=State.question,
                        on_change=State.set_question,
                        height="50%",
                        max_height="70%",
                        placeholder="Pregunta lo que quieras",
                        required=True,
                        type="text",
                    ),
                    # Botón de enviar.
                    rx.icon_button(
                        "arrow_up",
                        radius="full",
                    ),
                    bg="lightgray",
                    border_top_left_radius="16px",
                    border_top_right_radius="16px",
                    height="11vh",
                    on_submit=State.answer,
                    padding="16px",
                    reset_on_submit=True,
                    shadow = "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                    width="100%",
                ),
            width="100%",
        ),
        spacing="0",
        width="100vw",
    ),
)

app=rx.App()
app.add_page(index)