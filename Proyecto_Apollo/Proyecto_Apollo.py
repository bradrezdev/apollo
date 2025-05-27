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
            rx.markdown(answer, style=style.answer_style),
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
                                "Bryan Nuñez",
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
                rx.text("TelemedicinAI", align="center", weight="bold"),
                position="fixed",
                top=0,
                z_index=100,
                bg="rgba(255, 255, 255, 0.35)",
                style={
                    "backdropFilter": "blur(60px)",
                    "-webkit-backdrop-filter": "blur(60px)",
                },
                height="8vh",
                width="80%",
            ),
            # Imagen banner NN Protect.
            # Sección de chat.
            rx.center(
                rx.vstack(
                    rx.box(
                        rx.image(
                            src="/banner_web.jpg",
                            border_radius="16px",
                            width="100%",
                            height="100%",
                            style={"objectFit": "cover"},
                        ),
                        height="16vh",
                        margin_top="10vh",
                        width="98%",
                    ),
                    chat(),
                    height="85vh",
                    overflow_y="auto",
                    max_width="80%",
                    margin_bottom="1vh",
                    min_width="50%",
                ),
            ),
            # Sección de pregunta al chat.
            rx.center(
                rx.hstack(
                    # Input de pregunta al asistente.
                    rx.text_area(
                        value=State.question,
                        on_change=State.set_question,
                        align_self="flex-end",
                        auto_height=True,
                        border_radius="12px",
                        max_length=300,
                        placeholder="Pregunta lo que quieras",
                        required=True,
                        resize="vertical",
                        #rows="1",
                        style={"overflowY": "auto", "alignSelf": "flex-end"},
                        type="text",
                        width="100%",
                    ),
                    # Botón de enviar.
                    rx.icon_button(
                        "arrow_up",
                        bg="#0984e3",
                        on_click=State.answer,
                        radius="full",
                        size="3",
                    ),
                    align_self="flex-end",
                    auto_height=True,
                    bg="#ecf0f1",
                    border_radius="16px",
                    min_width="50%",
                    padding="16px",
                    reset_on_submit=True,
                    style={"overflowY": "auto", "alignSelf": "flex-end"},
                    width="80%",
                ),
            width="100%",
        ),
        spacing="0",
        width="100vw",
    ),
)

app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="teal"
    )
)
app.add_page(index)