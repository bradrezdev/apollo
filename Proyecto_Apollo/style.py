import reflex as rx
from reflex import State
from supabase_client import supabase

# Common style base
chat_margin = "40%"
message_style = dict(
    padding="1em",
    border_radius="12px",
    margin_y="0.5em",
    display="inline-block",
)

# Styles for questions and answers
question_style = message_style | dict(
    margin_left=chat_margin,
    margin_right="16px",
    background_color=rx.color("gray", 4),
    max_width="58.6%",

)
answer_style = message_style | dict(
    margin_left="16px",
)

class AuthState(State):
    email: str
    password: str
    error: str = ""
    success: str = ""

    def register(self):
        response = supabase.auth.sign_up({
            "email": self.email,
            "password": self.password
        })

        if response.get("error"):
            self.error = response["error"]["message"]
        else:
            self.success = "Registro exitoso. Revisa tu correo."

    def login(self):
        response = supabase.auth.sign_in_with_password({
            "email": self.email,
            "password": self.password
        })

        if response.get("error"):
            self.error = response["error"]["message"]
        else:
            self.success = "¡Login exitoso!"
            # Aquí podrías guardar el token y navegar a otra página