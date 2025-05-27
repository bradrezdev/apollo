import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import reflex as rx
from reflex import State
from supabase_client import supabase

load_dotenv()

class State(rx.State):
    question: str
    chat_history: list[tuple[str, str]] = []

    async def answer(self):
        message = self.question
        client = AsyncOpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )

        thread = await client.beta.threads.create()

        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        # Start streaming response from assistant
        session = await client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_wbg01t4JFYx0AVal09mtljlS",
            stream=True,
        )

        # Initialize response and update UI
        answer = ""
        self.chat_history.append((message, answer))
        self.question = ""
        yield

        # Process streaming response
        async for event in session:
            if event.event == "thread.message.delta" and event.data.delta.content:
                for content_block in event.data.delta.content:
                    if content_block.type == "text" and content_block.text and content_block.text.value:
                        answer += content_block.text.value
                        self.chat_history[-1] = (
                            self.chat_history[-1][0],
                            answer,
                        )
                        yield

class AuthState(rx.State):
    email: str
    password: str
    error: str = ""
    success: str = ""
    token: str = ""

    async def register(self):
        try:
            response = supabase.auth.sign_up({
                "email": self.email,
                "password": self.password
            })
            if response.get("error"):
                self.error = response["error"]["message"]
            else:
                self.success = "Registro exitoso. Revisa tu correo."
        except Exception as e:
            self.error = str(e)

    async def login(self):
        try:
            response = supabase.auth.sign_in_with_password({
                "email": self.email,
                "password": self.password
            })
            if response.get("error"):
                self.error = response["error"]["message"]
            else:
                self.success = "¡Login exitoso!"
                self.token = response["session"]["access_token"]
        except Exception as e:
            self.error = str(e)