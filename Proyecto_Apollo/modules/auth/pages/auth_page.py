import reflex as rx
from Proyecto_Apollo.styles.colors import *
from Proyecto_Apollo.styles import fonts
from Proyecto_Apollo.components.ui import button, input, badge
from ..state.auth_state import AuthState

def auth_page_ui() -> rx.Component:
    return rx.box(
        # ── Fixed particle canvas background ────────────────
        # Matches onano_website: canvas inside a fixed wrapper,
        # pointer-events=none so clicks pass through to forms.
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
        # ── Scripts ─────────────────────────────────────────
        # particle_hero.js auto-boots via its IIFE MutationObserver
        # and writes to window.__oParticleHero. 
        # apollo_particle_bridge.js provides window.animateParticleScroll.
        #rx.script(src="/scripts/particle_hero.js"),
        #rx.script(src="/scripts/apollo_particle_bridge.js"),
        # ── Horizontal slide container ──────────────────────
        # All steps exist in a row. Only the text/forms slide
        # horizontally; the canvas stays fixed behind everything.
        rx.box(
            rx.hstack(
                _render_step(step_login()),
                _render_step(step_initial()),
                _render_step(step_register()),
                _render_step(
                    step_transition(
                        "Creando nueva cuenta",
                        "Ya casi terminamos con tu registro",
                    )
                ),
                _render_step(step_profile()),
                _render_step(
                    step_transition(
                        "Preparando tu asistente personal",
                        AuthState.final_message,
                    )
                ),
                width="600vw",
                margin="0",
                padding="0",
                spacing="0",
                transform=f"translateX(calc(-100vw * {AuthState.step}))",
                transition="transform 0.8s cubic-bezier(0.4, 0, 0.2, 1)",
            ),
            bg=rx.color_mode_cond(
                light=BRAND_WHITE,
                dark=BRAND_DARK,
            ),
            #backdrop_filter="blur(64px)",
            width="100vw",
            overflow="hidden",
            position="relative",
            z_index="1",
        ),
        # ── Alert Dialog para error de login (solo móvil) ───
        rx.box(
            _render_login_error_dialog(),
            display=["none", "block", "block"],
        ),
        # Root styles
        width="100vw",
    )


# ── Step 0: Login ──────────────────────────────────────────
def step_login() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            button(
                rx.icon("chevron-right", size=24),
                on_click=AuthState.go_back,
                variant="ghost",
                width="auto",
                padding="0.5em",
                border_radius="50%",
            ),
            rx.heading(
                "Iniciar sesión",
                color=rx.color_mode_cond(
                    light=BRAND_PRIMARY_100,
                    dark=BRAND_WHITE,
                ),
                style=fonts.STYLE_H2,
            ),
            align="center",
            width="100%",
            spacing="2",
        ),
        rx.vstack(
            input(
                placeholder="Correo electrónico",
                type="email",
                value=AuthState.email,
                on_change=AuthState.set_email,
            ),
            input(
                placeholder="Contraseña",
                type="password",
                value=AuthState.password,
                on_change=AuthState.set_password,
            ),
            width="100%",
            spacing="4",
            margin_y="4",
        ),
        button(
            "Iniciar sesión",
            disabled=(AuthState.email == "") | (AuthState.password == ""),
            on_click=AuthState.submit_login,
            margin_top="4",
        ),
        spacing="6",
        align="start",
        padding="0 2em",
        justify="center",
        width="100%",
        max_width="450px",
    )


# ── Step 1: Welcome / Initial ─────────────────────────────
def step_initial() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.color_mode_cond(
                light=rx.image(src="/light-logo.svg", height="6em", margin_bottom="4em"),
                dark=rx.image(src="/dark-logo1.svg", height="6em", margin_bottom="4em"),
            ),
            width="100%",
            justify="center",
        ),
        rx.heading(
            "Bienvenido a Apollo",
            color=rx.color_mode_cond(
                light=BRAND_PRIMARY_100,
                dark=BRAND_WHITE,
            ),
            style=fonts.STYLE_H2,
        ),
        rx.text(
            "Tu asistente personal potenciado por la nanotecnología de ONANO®",
            color=rx.color_mode_cond(
                light=BRAND_PRIMARY_100,
                dark=BRAND_WHITE,
            ),
            style=fonts.STYLE_BODY,
            margin_bottom="1em",
        ),
        rx.vstack(
            button(
                "Iniciar sesión",
                on_click=AuthState.go_to_login,
                variant="outline",
            ),
            button(
                "Registrarse",
                on_click=AuthState.go_to_register,
                variant="primary",
            ),
            margin_top="2em",
            spacing="4",
            width="100%",
        ),
        padding="0 2em",
        justify="center",
        width="100%",
    )


# ── Step 2: Register Form ─────────────────────────────────
def step_register() -> rx.Component:
    return rx.form(
        rx.hstack(
            button(
                rx.icon("chevron-left", size=32),
                on_click=AuthState.go_back,
                variant="ghost",
                width="auto",
                padding="0.5em",
                border_radius="50%",
            ),
            rx.heading(
                "Crear cuenta",
                color=rx.color_mode_cond(
                    light=BRAND_PRIMARY_100,
                    dark=BRAND_WHITE,
                ),
                style=fonts.STYLE_H2,
            ),
            align="center",
            width="100%",
            spacing="2",
        ),
        rx.vstack(
            input(
                placeholder="Correo electrónico",
                type="email",
                value=AuthState.email,
                on_change=AuthState.set_email,
            ),
            input(
                placeholder="Contraseña",
                type="password",
                value=AuthState.password,
                on_change=AuthState.set_password,
            ),
            rx.box(
                badge("Una letra minúscula", AuthState.has_lowercase),
                badge("Una letra mayúscula", AuthState.has_uppercase),
                badge("Un número", AuthState.has_number),
                badge("Un símbolo especial", AuthState.has_special),
                badge("Mínimo 8 caracteres", AuthState.is_length_valid),
                padding_x="16px",
                width="100%",
                spacing="2",
            ),
            input(
                placeholder="Confirmar contraseña",
                type="password",
                value=AuthState.confirm_password,
                on_change=AuthState.set_confirm_password,
            ),
            rx.checkbox(
                "Acepto los Términos y Condiciones, autorizando el tratamiento de mis datos personales de acuerdo a la normativa legal vigente para el uso de esta plataforma.",
                checked=AuthState.terms_accepted,
                on_change=AuthState.set_terms_accepted,
                color=rx.color_mode_cond(
                    light=BRAND_PRIMARY_100,
                    dark=BRAND_WHITE,
                ),
                style=fonts.STYLE_MICRO,
            ),
            width="100%",
            spacing="4",
        ),
        button(
            "Siguiente",
            type="submit",
            disabled=(AuthState.email == "")
            | (AuthState.password == "")
            | (AuthState.confirm_password == "")
            | ~AuthState.terms_accepted,
            margin_top="24px",
        ),
        on_submit=AuthState.submit_step1,
        spacing="6",
        align="start",
        padding="2.5em 2em",
        justify="center",
        width="100%",
        max_width="450px",
    )


# ── Steps 3/5: Transition Loading ─────────────────────────
def step_transition(title: str, subtitle: str) -> rx.Component:
    return rx.vstack(
        rx.spinner(size="3", color=BRAND_WHITE),
        rx.heading(
            title,
            color=BRAND_WHITE,
            style=fonts.STYLE_H2,
            margin_top="4",
        ),
        rx.text(
            subtitle,
            color="rgba(255,255,255,0.7)",
            style=fonts.STYLE_BODY,
        ),
        spacing="4",
        align="center",
        padding="3em",
    )


# ── Step 4: Profile Form ──────────────────────────────────
def step_profile() -> rx.Component:
    return rx.form(
        rx.hstack(
            button(
                rx.icon("chevron-left", size=32),
                # Regresa al paso 2 (registro) para que el usuario pueda editar email/contraseña si quiere.
                on_click=AuthState.go_to_register,
                variant="ghost",
                width="auto",
                padding="0.5em",
                border_radius="50%",
            ),
            rx.heading(
                "Información personal",
                color=BRAND_WHITE,
                style=fonts.STYLE_H2,
            ),
            align="center",
            width="100%",
            spacing="2",
        ),
        rx.text(
            "Completa tu perfil para continuar",
            color="rgba(255,255,255,0.7)",
            style=fonts.STYLE_BODY,
            margin_bottom="16px",
        ),
        rx.vstack(
            input(
                placeholder="Nombre(s)",
                value=AuthState.first_name,
                on_change=AuthState.set_first_name,
            ),
            input(
                placeholder="Apellido(s)",
                value=AuthState.last_name,
                on_change=AuthState.set_last_name,
            ),
            input(
                placeholder="Fecha de nacimiento",
                type="date",
                value=AuthState.dob,
                on_change=AuthState.set_dob,
            ),
            width="100%",
            spacing="4",
        ),
        button(
            "Finalizar",
            type="submit",
            disabled=(AuthState.first_name == "")
            | (AuthState.last_name == "")
            | (AuthState.dob == ""),
            margin_top="32px",
        ),
        on_submit=AuthState.submit_step3,
        align="start",
        padding="3em",
        width="100%",
        max_width="450px",
    )


def _render_step(component: rx.Component) -> rx.Component:
    """Wrapper: cada paso ocupa 100vw y está centrado verticalmente."""
    return rx.center(
        rx.script("""
            // === 1. Bloquear touchmove fuera del chat ===
            document.addEventListener('touchmove', function(e) {
                let node = e.target;
                while (node && node !== document.body) {
                    if (node.classList && node.classList.contains('chat-scroll-area')) {
                        return;
                    }
                    node = node.parentNode;
                }
                e.preventDefault();
            }, { passive: false });

            // === 2. Ajustar --app-height con visualViewport ===
            function setAppHeight() {
                var vh = window.visualViewport ? window.visualViewport.height : window.innerHeight;
                document.documentElement.style.setProperty('--app-height', vh + 'px');
            }
            setAppHeight();
            if (window.visualViewport) {
                window.visualViewport.addEventListener('resize', setAppHeight);
                window.visualViewport.addEventListener('scroll', function() {
                    // Forzar scroll del viewport a 0 para evitar que iOS mueva la página
                    window.scrollTo(0, 0);
                });
            }
            window.addEventListener('resize', setAppHeight);
        """),
        component,
        width="100vw",
        height="100vh",
        flex_shrink="0",
        position="relative",
    )


def _render_login_error_dialog() -> rx.Component:
    """Renderiza el Alert Dialog para error de login (solo móvil)."""
    return rx.cond(
        AuthState.show_login_error,
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title(
                    "Error de inicio de sesión",
                    style=fonts.STYLE_H2,
                    margin_bottom="1em",
                ),
                rx.dialog.description(
                    "No hay un registro que coincida con este correo y/o contraseña.",
                    style=fonts.STYLE_BODY,
                ),
                button(
                    "Cerrar",
                    variant="primary",
                    height="48px",
                    margin_top="2em",
                    width="100%",
                    on_click=AuthState.close_login_error,
                ),
                style={
                    "padding": "2em",
                    "max_width": "320px",
                    "border_radius": "32px",
                    "display": ["block", "none", "none"],
                },
            ),
            open=AuthState.show_login_error,
        ),
    )


