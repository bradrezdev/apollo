"""
Componente reutilizable: Drawer de perfil de usuario.

Muestra nombre, email y botón de cerrar sesión en un drawer
que aparece desde abajo (direction="bottom") con esquinas
superiores redondeadas.

Uso:
    from Proyecto_Apollo.components.ui import user_profile_drawer, user_profile_trigger

    # Trigger (colócalo donde quieras abrir el drawer)
    user_profile_trigger()

    # Drawer (colócalo una vez en el layout)
    user_profile_drawer()
"""

import reflex as rx
from Proyecto_Apollo.styles.colors import (
    BRAND_PRIMARY_100,
    BRAND_SECONDARY_100,
    BRAND_WHITE,
    BRAND_TEXT_DARK,
    BRAND_BACKGROUND_ALT,
    BRAND_BORDER_SOFT,
    BRAND_ERROR,
)
from Proyecto_Apollo.styles.common_styles import glassmorphism_style


# ── Styles ────────────────────────────────────────────────────────────

_drawer_content_style = {
    **glassmorphism_style,
    "border_radius": "24px 24px 0 0",
    "padding": "1.5rem",
    "width": "100%",
    "max_width": "480px",
    "margin": "0 auto",
}

_avatar_style = {
    "background": rx.color_mode_cond(
        light=BRAND_PRIMARY_100,
        dark=BRAND_SECONDARY_100,
    ),
    "color": BRAND_WHITE,
    "border_radius": "50%",
    "width": "48px",
    "height": "48px",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "font_size": "1.25rem",
    "font_weight": "bold",
    "flex_shrink": "0",
}

_user_name_style = {
    "size": "4",
    "weight": "bold",
    "color": rx.color_mode_cond(
        light=BRAND_TEXT_DARK,
        dark=BRAND_WHITE,
    ),
}

_user_email_style = {
    "size": "2",
    "weight": "medium",
    "color": rx.color_mode_cond(
        light=BRAND_PRIMARY_100,
        dark=BRAND_SECONDARY_100,
    ),
}

_logout_button_style = {
    "width": "100%",
    "border_radius": "12px",
    "padding": "0.75rem",
    "cursor": "pointer",
    "transition": "all 0.2s ease",
    "color": BRAND_ERROR,
    "bg": rx.color_mode_cond(
        light=f"{BRAND_ERROR}10",
        dark=f"{BRAND_ERROR}15",
    ),
    "_hover": {
        "bg": rx.color_mode_cond(
            light=f"{BRAND_ERROR}20",
            dark=f"{BRAND_ERROR}25",
        ),
    },
}

_close_button_style = {
    "position": "absolute",
    "top": "1rem",
    "right": "1rem",
}


# ── Components ────────────────────────────────────────────────────────

def _user_avatar(user_name: rx.Var[str]) -> rx.Component:
    """Avatar circular con la inicial del nombre del usuario."""
    return rx.box(
        rx.text(
            rx.cond(
                user_name != "",
                user_name.to(str)[0].upper(),  # type: ignore
                "U",
            ),
            size="4",
            weight="bold",
        ),
        **_avatar_style,
    )


def user_profile_drawer(
    *,
    user_name: rx.Var,
    user_email: rx.Var,
    is_open: rx.Var[bool],
    on_open_change: rx.EventHandler,
    on_logout: rx.EventHandler,
) -> rx.Component:
    """
    Drawer de perfil de usuario (direction=bottom).

    Args:
        user_name:       Var con el nombre completo del usuario.
        user_email:      Var con el email del usuario.
        is_open:         Var[bool] que controla si el drawer está abierto.
        on_open_change:  EventHandler para toggle del drawer.
        on_logout:       EventHandler para cerrar sesión.
    """
    return rx.drawer.root(
        rx.drawer.overlay(z_index="9998"),
        rx.drawer.portal(
            rx.drawer.content(
                # Close button
                rx.drawer.close(
                    rx.icon_button(
                        rx.icon("x", size=20),
                        variant="ghost",
                        size="2",
                        cursor="pointer",
                        color=rx.color_mode_cond(
                            light=BRAND_TEXT_DARK,
                            dark=BRAND_WHITE,
                        ),
                    ),
                    style=_close_button_style,
                ),

                rx.vstack(
                    # Avatar + info
                    rx.vstack(
                        _user_avatar(user_name),
                        rx.text(user_name, **_user_name_style),
                        rx.text(user_email, **_user_email_style),
                        align="center",
                        spacing="2",
                        width="100%",
                        padding_top="0.5rem",
                    ),

                    rx.divider(
                        color=rx.color_mode_cond(
                            light=BRAND_BORDER_SOFT,
                            dark=BRAND_BORDER_SOFT,
                        ),
                        margin_y="0.75rem",
                    ),

                    # Logout button
                    rx.button(
                        rx.icon("log-out", size=18),
                        rx.text("Cerrar sesión", size="3", weight="medium"),
                        variant="ghost",
                        on_click=on_logout,
                        **_logout_button_style,
                    ),

                    spacing="3",
                    width="100%",
                    align="center",
                    padding_bottom="1rem",
                ),

                **_drawer_content_style,
                z_index="9999",
            ),
        ),
        direction="bottom",
        open=is_open,
        on_open_change=on_open_change,
    )


def user_profile_trigger(
    *,
    user_name: rx.Var,
    user_email: rx.Var,
    on_click: rx.EventHandler,
) -> rx.Component:
    """
    Trigger reutilizable que muestra nombre + email + chevron para abrir
    el drawer de perfil.

    Args:
        user_name:  Var con el nombre del usuario.
        user_email: Var con el email del usuario.
        on_click:   EventHandler para abrir el drawer.
    """
    return rx.hstack(
        rx.icon_button(
            rx.icon("user"),
            size="3",
            radius="full",
            variant="soft",
            color_scheme="blue",
            cursor="pointer",
            on_click=on_click,
        ),
        rx.vstack(
            rx.text(
                user_name,
                size="3",
                weight="bold",
                color=rx.color_mode_cond(
                    light=BRAND_TEXT_DARK,
                    dark=BRAND_WHITE,
                ),
            ),
            rx.text(
                user_email,
                size="1",
                weight="medium",
                color=rx.color_mode_cond(
                    light=BRAND_PRIMARY_100,
                    dark=BRAND_SECONDARY_100,
                ),
            ),
            spacing="0",
            width="100%",
            on_click=on_click,
            cursor="pointer",
        ),
        rx.spacer(),
        rx.icon(
            "chevron-right",
            size=18,
            color=rx.color_mode_cond(
                light=BRAND_TEXT_DARK,
                dark=BRAND_WHITE,
            ),
            cursor="pointer",
            on_click=on_click,
        ),
        width="100%",
        align="center",
        padding="0.25rem",
        border_radius="12px",
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "bg": rx.color_mode_cond(
                light=BRAND_BACKGROUND_ALT,
                dark=BRAND_BACKGROUND_ALT,
            ),
        },
    )
