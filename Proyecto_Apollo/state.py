import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import reflex as rx
from Proyecto_Apollo.api_keys import OPENAI_API_KEY
from Proyecto_Apollo.api_keys import API_ASSISTANT_ID

load_dotenv()

class State(rx.State):
    question: str
    chat_history: list[tuple[str, str]] = []

    async def answer(self):
        message = self.question
        client = AsyncOpenAI(
            api_key=OPENAI_API_KEY
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
            assistant_id=API_ASSISTANT_ID,
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