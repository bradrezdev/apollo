import os
from openai import AsyncOpenAI
import reflex as rx
from dotenv import load_dotenv

load_dotenv()


class State(rx.State):
    # La pregunta que está siendo hecha.
    question: str

    # Sigue el rastro del historial del chat como una lista de tuplas (pregunta, respuesta).
    chat_history: list[tuple[str, str]]

    async def answer(self):
        client = AsyncOpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )

        session = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": self.question}
            ],
            stop=None,
            temperature=0.7,
            stream=True,
        )

        answer = ""
        self.chat_history.append((self.question, answer))

        # Limpiar la pregunta actual del input
        self.question = ""

        # Hacer yield para que el frontend se actualice
        yield

        async for item in session:
            if hasattr(item.choices[0].delta, "content"):
                if item.choices[0].delta.content is None:
                    # presence of 'None' indicates the end of the response
                    break
                answer += item.choices[0].delta.content
                self.chat_history[-1] = (
                    self.chat_history[-1][0],
                    answer,
                )
                yield

    def auto_scroll(self):
        return rx.auto_scroll(
            rx.foreach(
                self.chat_history,
                lambda message: rx.box(
                    rx.text(f"Usuario: {message[0]}"),
                    rx.text(f"Asistente: {message[1]}"),
                    padding="0.5em",
                    border_bottom="1px solid #eee",
                    width="100%",
                ),
            ),
            height="400px",
            width="100%",
            border="1px solid #ddd",
            border_radius="md",
            padding="1em",
            key=len(self.chat_history),  # <- Esto obliga a re-renderizar
            overflow_y="auto",
        )