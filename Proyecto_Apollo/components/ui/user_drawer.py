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
from Proyecto_Apollo.styles.fonts import *
from Proyecto_Apollo.styles.common_styles import glassmorphism_style


# ── Styles ────────────────────────────────────────────────────────────

_drawer_content_style = {
    **glassmorphism_style,
    # Esquinas superiores redondeadas en mobile/tablet; todas redondeadas en desktop
    "border_radius": ["32px 32px 0 0", "32px 32px 0 0", "32px", "32px"],
    "padding": "1.5rem",
    "width": ["100%", "100%", "480px", "480px"],
    "max_width": "480px",
    "margin": "0 auto",
    # Altura responsiva: [mobile, tablet, desktop, large desktop]
    "height": ["95dvh", "95dvh", "auto", "auto"],
    # Centrado vertical en desktop — Radix posiciona bottom:0 por defecto;
    # en desktop sobreescribimos para centrar en el viewport.
    "min_height": ["unset", "unset", "300px", "300px"],
    "max_height": ["95dvh", "95dvh", "70dvh", "60dvh"],
    # Centering override for desktop (Radix drawer content is position:fixed)
    "bottom": ["0", "0", "unset", "unset"],
    "top": ["unset", "unset", "50%", "50%"],
    "left": ["unset", "unset", "50%", "50%"],
    "transform": ["unset", "unset", "translate(-50%, -50%)", "translate(-50%, -50%)"],
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
    "font_style": STYLE_BODY,
    "color": rx.color_mode_cond(
        light=BRAND_TEXT_DARK,
        dark=BRAND_WHITE,
    ),
}

_user_email_style = {
    "font_style": STYLE_LABEL,
    "color": rx.color_mode_cond(
        light=BRAND_PRIMARY_100,
        dark=BRAND_SECONDARY_100,
    ),
}

_logout_button_style = {
    "width": "100%",
    "border_radius": "32px",
    "padding_y": "16px",
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
        rx.drawer.overlay(
            z_index="9998",
        ),
        rx.drawer.portal(
            rx.drawer.content(
                # Close button
                rx.drawer.close(
                    rx.icon_button(
                        rx.icon("x", size=16),
                        radius="full",
                        variant="soft",
                        bg=rx.color_mode_cond(
                            light=BRAND_WHITE,
                            dark=BRAND_BACKGROUND_ALT,
                        ),
                        color=rx.color_mode_cond(
                            light=BRAND_TEXT_DARK,
                            dark=BRAND_WHITE,
                        ),
                        width="auto",
                        height="auto",
                        padding="0.75rem",
                        cursor="pointer",
                    ),
                    style=_close_button_style,
                ),

                # Título del drawer
                rx.text(
                    "Perfil de usuario",
                    font_style=STYLE_LABEL,
                    width="90%",
                    text_align="center",
                    position="absolute",
                ),

                rx.vstack(
                    # Avatar + info
                    rx.hstack(
                        _user_avatar(user_name),
                        rx.vstack(
                            rx.text(user_name, **_user_name_style),
                            rx.text(user_email, **_user_email_style),
                        ),
                        bg=rx.color_mode_cond(
                            light=BRAND_WHITE,
                            dark=BRAND_BACKGROUND_ALT,
                        ),
                        align="center",
                        border_radius="32px",
                        padding="8px 12px",
                        spacing="4",
                        height="auto",
                        width="100%",
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
                    padding_top="4rem",
                    padding_bottom="1rem",
                ),
                **_drawer_content_style,
                z_index="9999",
            ),
        ),
        #snap_points=[0.85, 0.6],  # Ajustes de snap [float inicial al abrir('85%'), float al que se puede minimizar('60%')]
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
        _user_avatar(user_name),
        rx.vstack(
            rx.text(user_name, **_user_name_style),
            rx.text(user_email, **_user_email_style),
            spacing="0",
            width="100%",
            on_click=on_click,
            cursor="pointer",
        ),
        rx.spacer(),
        rx.icon(
            "chevron-right",
            size=32,
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
        border_radius="32px",
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "bg": rx.color_mode_cond(
                light=BRAND_BACKGROUND_ALT,
                dark=BRAND_BACKGROUND_ALT,
            ),
        },
    )
