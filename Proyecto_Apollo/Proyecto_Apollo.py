import reflex as rx
from Proyecto_Apollo import style

def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(question, text_align="right"),
        rx.box(answer, text_align="left"),
        margin="1em",
        )

def chat() -> rx.Component:
    qa_pairs = [
        (
            "¿Qué es Reflex?",
            "Una manera de construir aplicaciones web en Python.",
        ),
        (
            "¿Qué puedo hacer con Reflex?",
            "Todo lo que puedes hacer con React, pero en Python.",
        ),
    ]
    return rx.box(
        *[
            qa(question, answer)
            for question, answer in qa_pairs
        ]
    )

def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Haz una pregunta"),
        rx.button("Preguntar"),
    )

def index() -> rx.Component:
    return rx.container(
        chat(),
        action_bar(),
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)