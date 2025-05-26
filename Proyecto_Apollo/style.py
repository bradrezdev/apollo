import reflex as rx

# Common style base
shadow = "rgba(0, 0, 0, 0.15) 0px 2px 8px"
chat_margin = "20%"
message_style = dict(
    padding="1em",
    border_radius="5px",
    margin_y="0.5em",
    box_shadow=shadow,
    max_width="30em",
    display="inline-block",
)

# Styles for questions and answers
question_style = message_style | dict(
    margin_left=chat_margin,
    margin_right="16px",
    background_color=rx.color("gray", 4),
)
answer_style = message_style | dict(
    margin_left="16px",
    margin_right=chat_margin,
    background_color=rx.color("accent", 8),
)