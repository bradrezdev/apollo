import reflex as rx

chat_margin = "28%"
message_style = dict(
    padding="1em",
    border_radius="16px",
    margin_y="0.5em",
    max_width="30em",
    display="inline-block",
)

question_style = message_style | dict(
    margin_left=chat_margin,
    background_color=rx.color("gray", 4),
)
answer_style = message_style | dict(
    margin_right=chat_margin,
    background_color=rx.color("accent", 8),
)

input_style = dict(
    border_radius="8px",
    border_width="1px",
    padding="0.5em",
    width="350px",
)
button_style = dict(
    background_color=rx.color("accent", 10),
        border_radius="8px",
)