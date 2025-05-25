import reflex as rx 

class State(rx.State):
    pass

def index():
    return rx.hstack(
        # Sidebar menu.
        rx.center(
            "Sidebar",
            bg="gray",
            height="100vh",
            width="20vw",
        ),
        # Sección de chat.
        rx.vstack(
            # Header TelemedicinAI.
            rx.container(
                "TelemedicinAI",
                bg="gold",
                height="8vh",
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
                height="56vh"
            ),
            # Sección de pregunta al chat.
            rx.hstack(
                # Input de pregunta al asistente.
                rx.input(
                    bg="lightgray",
                    height="50%",
                    max_height="70%",
                    name="Pregunta",
                    placeholder="Pregunta lo que quieras",
                    type="text",
                    required=True,
                    width="80%",
                ),
                # Botón de enviar.
                rx.button(
                    "Enviar",
                    height="50%",
                    type="submit",
                    width="20%",
                ),
                bg="lightgray",
                height="12vh",
                width="100%",
            ),
            spacing="4",
            width="80vw",
        ),
        bg="#000",
        spacing="0",
        width="100vw",
    )

app=rx.App()
app.add_page(index)