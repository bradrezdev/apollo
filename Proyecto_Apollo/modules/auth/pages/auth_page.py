import reflex as rx
from Proyecto_Apollo.styles.colors import *
from Proyecto_Apollo.styles import fonts
from Proyecto_Apollo.components.ui import button, input, badge
from ..state.auth_state import AuthState


def auth_page_ui() -> rx.Component:
    return rx.box(
        # Fixed particle canvas background
        rx.box(
            rx.el.canvas(
                id="particle-hero-canvas",
                style={
                    "display": "block",
                    "width": "100%",
                    "height": "100vh",
                },
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            z_index="0",
            pointer_events="none",
        ),
        # Main content
        rx.center(
            rx.vstack(
                # Logo
                rx.hstack(
                    rx.color_mode_cond(
                        light=rx.image(src="/light-logo.svg", height="6em", margin_bottom="1em"),
                        dark=rx.image(src="/dark-logo1.svg", height="6em", margin_bottom="1em"),
                    ),
                    width="100%",
                    justify="center",
                ),
                # Segmented control
                rx.segmented_control.root(
                    rx.segmented_control.item(
                        "Registro", value="registro"
                    ),
                    rx.segmented_control.item(
                        "Iniciar sesión", value="iniciar_sesion"
                    ),
                    value=AuthState.segment,
                    on_change=AuthState.setvar("segment"),
                    variant="surface",
                    radius="full",
                    width="100%",
                    margin_bottom="1.5em",
                ),
                # Segment content
                rx.cond(
                    AuthState.segment == "registro",
                    _render_register_segment(),
                    _render_login_segment(),
                ),
                spacing="6",
                align="center",
                max_width="400px",
                width="100%",
                padding="2em",
            ),
            width="100vw",
            height="100dvh",
            position="relative",
            z_index="1",
        ),
        # Name form overlay (post-login)
        rx.cond(
            AuthState.show_name_form,
            _render_name_form_overlay(),
        ),
        # Loading animation overlay
        rx.cond(
            AuthState.loading_step > 0,
            _render_loading_overlay(),
        ),
        width="100vw",
    )


# ── Registration Segment ────────────────────────────────
def _render_register_segment() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Crear cuenta",
            color=rx.color_mode_cond(
                light=BRAND_PRIMARY_100,
                dark=BRAND_WHITE,
            ),
            style=fonts.STYLE_H1,
            text_align="center",
        ),
        rx.text(
            "Regístrate para comenzar",
            color=rx.color_mode_cond(
                light=BRAND_PRIMARY_60,
                dark="rgba(255,255,255,0.7)",
            ),
            style=fonts.STYLE_BODY,
            text_align="center",
            margin_bottom="1.5em",
        ),
        # Email input (always visible)
        input(
            placeholder="Correo electrónico",
            type="email",
            value=AuthState.email,
            on_change=AuthState.set_email,
        ),
        # Progressive reveal: password fields
        rx.cond(
            AuthState.show_extra_fields,
            rx.vstack(
                # Password
                input(
                    placeholder="Contraseña",
                    type="password",
                    value=AuthState.password,
                    on_change=AuthState.set_password,
                ),
                # Password requirements badges
                rx.cond(
                    AuthState.password != "",
                    rx.box(
                        badge("a-z", AuthState.has_lowercase),
                        badge("A-Z", AuthState.has_uppercase),
                        badge("0-9", AuthState.has_number),
                        badge("#$", AuthState.has_special),
                        badge("8+", AuthState.is_length_valid),
                        flex_wrap="wrap",
                        justify_content="center",
                        spacing="2",
                        margin_top="0.5em",
                    ),
                ),
                # Confirm password
                input(
                    placeholder="Confirmar contraseña",
                    type="password",
                    value=AuthState.confirm_password,
                    on_change=AuthState.set_confirm_password,
                ),
                # Terms checkbox
                rx.hstack(
                    rx.checkbox(
                        checked=AuthState.terms_accepted,
                        on_change=AuthState.set_terms_accepted,
                    ),
                    rx.text(
                        "Acepto los Términos y Condiciones",
                        font_size="13px",
                        color=rx.color_mode_cond(
                            light=BRAND_PRIMARY_100,
                            dark=BRAND_WHITE,
                        ),
                    ),
                    spacing="2",
                    align="center",
                ),
                # Register button
                button(
                    "Registrar",
                    on_click=AuthState.submit_register,
                    loading=AuthState.is_loading,
                    width="100%",
                    margin_top="1em",
                ),
                spacing="4",
                align="center",
                width="100%",
            ),
        ),
        spacing="4",
        align="center",
        width="100%",
    )


# ── Login Segment ───────────────────────────────────────
def _render_login_segment() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Iniciar sesión",
            color=rx.color_mode_cond(
                light=BRAND_PRIMARY_100,
                dark=BRAND_WHITE,
            ),
            style=fonts.STYLE_H1,
            text_align="center",
        ),
        rx.text(
            "Accede a tu cuenta",
            color=rx.color_mode_cond(
                light=BRAND_PRIMARY_60,
                dark="rgba(255,255,255,0.7)",
            ),
            style=fonts.STYLE_BODY,
            text_align="center",
            margin_bottom="1.5em",
        ),
        # Email input (always visible)
        input(
            placeholder="Correo electrónico",
            type="email",
            value=AuthState.email,
            on_change=AuthState.set_email,
        ),
        # Progressive reveal: password + button
        rx.cond(
            AuthState.show_extra_fields,
            rx.vstack(
                input(
                    placeholder="Contraseña",
                    type="password",
                    value=AuthState.password,
                    on_change=AuthState.set_password,
                ),
                button(
                    "Iniciar sesión",
                    on_click=AuthState.submit_login,
                    loading=AuthState.is_loading,
                    width="100%",
                    margin_top="0.5em",
                ),
                spacing="4",
                align="center",
                width="100%",
            ),
        ),
        spacing="4",
        align="center",
        width="100%",
    )


# ── Name Form Overlay (Post-Login) ──────────────────────
def _render_name_form_overlay() -> rx.Component:
    return rx.box(
        rx.center(
            rx.vstack(
                rx.box(
                    rx.icon(
                        "user",
                        size=48,
                        color=BRAND_SECONDARY_100,
                    ),
                    margin_bottom="1em",
                ),
                rx.heading(
                    "Cuéntanos sobre ti",
                    color=rx.color_mode_cond(
                        light=BRAND_PRIMARY_100,
                        dark=BRAND_WHITE,
                    ),
                    style=fonts.STYLE_H1,
                    text_align="center",
                ),
                rx.text(
                    "Ingresa tu nombre para personalizar tu experiencia",
                    color=rx.color_mode_cond(
                        light=BRAND_PRIMARY_60,
                        dark="rgba(255,255,255,0.7)",
                    ),
                    style=fonts.STYLE_BODY,
                    text_align="center",
                    margin_bottom="1.5em",
                ),
                rx.vstack(
                    input(
                        placeholder="Nombre",
                        value=AuthState.first_name,
                        on_change=AuthState.set_first_name,
                    ),
                    input(
                        placeholder="Apellido",
                        value=AuthState.last_name,
                        on_change=AuthState.set_last_name,
                    ),
                    spacing="4",
                    width="100%",
                ),
                button(
                    "Continuar",
                    on_click=AuthState.submit_name,
                    loading=AuthState.is_loading,
                    width="100%",
                    margin_top="1.5em",
                ),
                spacing="4",
                align="center",
                max_width="400px",
                width="100%",
                padding="2em",
                bg=rx.color_mode_cond(
                    light=BRAND_WHITE,
                    dark=BRAND_HERO_BG,
                ),
                border_radius="24px",
                box_shadow="0px 8px 32px rgba(0, 0, 0, 0.15)",
            ),
            width="100vw",
            height="100dvh",
            bg=rx.color_mode_cond(
                light="rgba(255, 255, 255, 0.9)",
                dark="rgba(7, 13, 26, 0.95)",
            ),
        ),
        position="fixed",
        top="0",
        left="0",
        width="100vw",
        height="100vh",
        z_index="100",
    )


# ── Loading Animation Overlay ────────────────────────────
def _render_loading_overlay() -> rx.Component:
    return rx.box(
        rx.center(
            rx.vstack(
                rx.color_mode_cond(
                    light=rx.image(src="/light-logo.svg", height="4em", margin_bottom="2em"),
                    dark=rx.image(src="/dark-logo1.svg", height="4em", margin_bottom="2em"),
                ),
                rx.spinner(
                    size="3",
                    color=BRAND_SECONDARY_100,
                    margin_bottom="1.5em",
                ),
                rx.text(
                    AuthState.loading_message,
                    color=rx.color_mode_cond(
                        light=BRAND_PRIMARY_100,
                        dark=BRAND_WHITE,
                    ),
                    style=fonts.STYLE_H2,
                    text_align="center",
                ),
                spacing="4",
                align="center",
            ),
            width="100vw",
            height="100dvh",
            bg=rx.color_mode_cond(
                light="rgba(255, 255, 255, 0.98)",
                dark=BRAND_HERO_BG,
            ),
        ),
        position="fixed",
        top="0",
        left="0",
        width="100vw",
        height="100vh",
        z_index="100",
    )
