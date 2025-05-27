import reflex as rx

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