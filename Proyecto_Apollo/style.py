import reflex as rx

# Common style base
chat_margin = "40%"
message_style = dict(
    padding="2vh",
    border_radius="20px",
    #margin_y="0.5em",
    display="inline-block",
)

# Styles for questions and answers
question_style = message_style | dict(
    background_color="#ecf0f1",
    margin_left=chat_margin,
    margin_right="16px",
    max_width="58.6%",
    overflow_wrap="break-word",
    white_space="pre-wrap",
)
answer_style = message_style | dict(
    margin_left="16px",
)