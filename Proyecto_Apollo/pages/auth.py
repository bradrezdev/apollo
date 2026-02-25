import typing
import reflex as rx
import asyncio

from Proyecto_Apollo.styles.colors import SECONDARY_100, NEUTRAL_WHITE, SUCCESS
from Proyecto_Apollo.styles.fonts import FontSystem
from Proyecto_Apollo.components.ui.atoms import atom_button, atom_input, atom_badge



class AuthState(rx.State):
    """Estado para el flujo de autenticación y registro."""

    if typing.TYPE_CHECKING:
        set_email: typing.ClassVar[rx.EventHandler]
        set_password: typing.ClassVar[rx.EventHandler]
        set_confirm_password: typing.ClassVar[rx.EventHandler]
        set_first_name: typing.ClassVar[rx.EventHandler]
        set_last_name: typing.ClassVar[rx.EventHandler]
        set_dob: typing.ClassVar[rx.EventHandler]
        set_terms_accepted: typing.ClassVar[rx.EventHandler]

    # Steps: 0=login, 1=initial(welcome), 2=register, 3=transition, 4=profile, 5=final
    step: int = 1

    email: str = ""
    password: str = ""
    confirm_password: str = ""
    terms_accepted: bool = False

    first_name: str = ""
    last_name: str = ""
    dob: str = ""

    final_message: str = "Preparando tu asistente personal"

    def on_load(self):
        self.step = 1
        self.email = ""
        self.password = ""
        self.confirm_password = ""
        self.first_name = ""
        self.last_name = ""
        self.dob = ""
        self.terms_accepted = False
        # Reset particle state to phase-0 (agglomerated, gentle vibration)
        return rx.call_script(
            "window._apolloParticleProgress = 0;"
            "if(window.__oParticleHero){ window.__oParticleHero.setScrollProgress(0); }"
        )

    # ── Password validation computed vars ──────────────────
    @rx.var
    def has_lowercase(self) -> bool:
        return any(c.islower() for c in self.password)

    @rx.var
    def has_uppercase(self) -> bool:
        return any(c.isupper() for c in self.password)

    @rx.var
    def has_number(self) -> bool:
        return any(c.isdigit() for c in self.password)

    @rx.var
    def has_special(self) -> bool:
        return any(not c.isalnum() for c in self.password) and len(self.password) > 0

    @rx.var
    def is_length_valid(self) -> bool:
        return len(self.password) >= 8

    @rx.var
    def is_password_valid(self) -> bool:
        return (
            self.has_lowercase
            and self.has_uppercase
            and self.has_number
            and self.has_special
            and len(self.password) >= 8
        )

    @rx.var
    def passwords_match(self) -> bool:
        return self.password == self.confirm_password and len(self.password) > 0

    @rx.var
    def is_email_valid(self) -> bool:
        return "@" in self.email and "." in self.email.split("@")[-1]

    @rx.var
    def can_proceed_step1(self) -> bool:
        return (
            self.is_email_valid
            and self.is_password_valid
            and self.passwords_match
            and self.terms_accepted
        )

    # ── Navigation events ──────────────────────────────────
    @rx.event
    def go_to_register(self):
        """Welcome → Register (slide right). Particles: disperse to 0.5."""
        self.step = 2
        return rx.call_script("window.animateParticleScroll(0.5, 800);")

    @rx.event
    def go_to_login(self):
        """Welcome → Login (slide left). Particles: disperse to 0.5."""
        self.step = 0
        return rx.call_script("window.animateParticleScroll(0.5, 800);")

    @rx.event
    def go_back(self):
        """Any form → Welcome (slide back). Particles: re-agglomerate to 0."""
        self.step = 1
        return rx.call_script("window.animateParticleScroll(0.0, 800);")

    @rx.event
    async def submit_step1(self):
        """Register form submitted → transition → profile."""
        if self.can_proceed_step1:
            self.step = 3
            yield rx.call_script("window.animateParticleScroll(0.2, 800);")
            await asyncio.sleep(2)
            self.step = 4

    @rx.event
    async def submit_step3(self):
        """Profile submitted → final loading sequence."""
        if self.first_name and self.last_name and self.dob:
            self.step = 5
            self.final_message = "Cargando productos..."
            yield rx.call_script("window.animateParticleScroll(0.5, 1200);")
            yield
            await asyncio.sleep(2)

            self.final_message = "Cargando plan de compensación..."
            yield rx.call_script("window.animateParticleScroll(0.8, 1200);")
            yield
            await asyncio.sleep(2)

            self.final_message = "Cargando tu asistente personal..."
            yield rx.call_script("window.animateParticleScroll(1.0, 1200);")
            yield
            await asyncio.sleep(2)

            yield rx.redirect("/chat")


# ═══════════════════════════════════════════════════════════
#  UI COMPONENTS
# ═══════════════════════════════════════════════════════════

def _render_step(component: rx.Component) -> rx.Component:
    """Wrapper: cada paso ocupa 100vw y está centrado verticalmente."""
    return rx.center(
        component,
        width="100vw",
        height="100vh",
        flex_shrink="0",
        position="relative",
    )


def auth_page_ui() -> rx.Component:
    return rx.box(
        # ── Fixed particle canvas background ────────────────
        # Matches onano_website: canvas inside a fixed wrapper,
        # pointer-events:none so clicks pass through to forms.
        rx.box(
            rx.el.canvas(
                id="particle-hero-canvas",
                style={
                    "display": "block",
                    "width": "100%",
                    "height": "100%",
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
        rx.script(src="/scripts/particle_hero.js"),
        rx.script(src="/scripts/apollo_particle_bridge.js"),
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
                height="100vh",
                margin="0",
                padding="0",
                spacing="0",
                transform=f"translateX(calc(-100vw * {AuthState.step}))",
                transition="transform 0.8s cubic-bezier(0.4, 0, 0.2, 1)",
            ),
            width="100vw",
            height="100vh",
            overflow="hidden",
            position="relative",
            z_index="1",
        ),
        # Root styles
        width="100vw",
        height="100vh",
        overflow="hidden",
        bg="#070D1A",
    )


# ── Step 0: Login ──────────────────────────────────────────
def step_login() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            atom_button(
                rx.icon("chevron-right", size=24),
                on_click=AuthState.go_back,
                variant="ghost",
                width="auto",
                padding="0.5em",
                border_radius="50%",
            ),
            rx.heading(
                "Iniciar sesión",
                color=NEUTRAL_WHITE,
                font=FontSystem.SIZE_H2,
            ),
            align="center",
            width="100%",
            spacing="2",
        ),
        rx.vstack(
            atom_input(
                placeholder="Correo electrónico",
                type="email",
                value=AuthState.email,
                on_change=AuthState.set_email,
            ),
            atom_input(
                placeholder="Contraseña",
                type="password",
                value=AuthState.password,
                on_change=AuthState.set_password,
            ),
            width="100%",
            spacing="4",
            margin_y="4",
        ),
        atom_button(
            "Entrar",
            disabled=(AuthState.email == "") | (AuthState.password == ""),
            margin_top="4",
        ),
        spacing="6",
        align="start",
        padding="2.5em 2em",
        justify="center",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(16px)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="24px",
        width="100%",
        max_width="450px",
    )


# ── Step 1: Welcome / Initial ─────────────────────────────
def step_initial() -> rx.Component:
    return rx.vstack(
        rx.image(src="/dark-logo.svg", height="6em", margin_bottom="2em"),
        rx.heading(
            "Bienvenido a Apollo",
            color=NEUTRAL_WHITE,
            font=FontSystem.SIZE_H2,
        ),
        rx.text(
            "Tu asistente personal potenciado por la nanotecnología de ONANO®",
            color=NEUTRAL_WHITE,
            font=FontSystem.SIZE_BODY,
            margin_bottom="1em",
        ),
        rx.vstack(
            atom_button(
                "Iniciar sesión",
                on_click=AuthState.go_to_login,
                variant="outline",
            ),
            atom_button(
                "Registrarse",
                on_click=AuthState.go_to_register,
                variant="primary",
            ),
            margin_top="2em",
            spacing="4",
            width="100%",
        ),
        padding="0 10px",
        justify="center",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(16px)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        height="120vh",
        width="100%",
        max_width="400px",
    )


# ── Step 2: Register Form ─────────────────────────────────
def step_register() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            atom_button(
                rx.icon("chevron-left", size=24),
                on_click=AuthState.go_back,
                variant="ghost",
                width="auto",
                padding="0.5em",
                border_radius="50%",
            ),
            rx.heading(
                "Crear cuenta",
                color=NEUTRAL_WHITE,
                font=FontSystem.SIZE_H2,
            ),
            align="center",
            width="100%",
            spacing="2",
        ),
        rx.vstack(
            atom_input(
                placeholder="Correo electrónico",
                type="email",
                value=AuthState.email,
                on_change=AuthState.set_email,
            ),
            atom_input(
                placeholder="Contraseña",
                type="password",
                value=AuthState.password,
                on_change=AuthState.set_password,
            ),
            rx.box(
                atom_badge("Una letra minúscula", AuthState.has_lowercase),
                atom_badge("Una letra mayúscula", AuthState.has_uppercase),
                atom_badge("Un número", AuthState.has_number),
                atom_badge("Un símbolo especial", AuthState.has_special),
                atom_badge("Mínimo 8 caracteres", AuthState.is_length_valid),
                margin_y="4",
                padding="1.5em",
                background="rgba(255,255,255,0.05)",
                border_radius="16px",
                width="100%",
                spacing="2",
            ),
            atom_input(
                placeholder="Confirmar contraseña",
                type="password",
                value=AuthState.confirm_password,
                on_change=AuthState.set_confirm_password,
            ),
            rx.checkbox(
                "Acepto los Términos y Condiciones, autorizando el tratamiento de mis datos personales de acuerdo a la normativa legal vigente para el uso de esta plataforma.",
                checked=AuthState.terms_accepted,
                on_change=AuthState.set_terms_accepted,
                color="rgba(255,255,255,0.8)",
                font_size=FontSystem.SIZE_MICRO,
                font_family=FontSystem.SECONDARY_FONT,
            ),
            width="100%",
            spacing="4",
        ),
        atom_button(
            "Siguiente",
            on_click=AuthState.submit_step1,
            disabled=~AuthState.can_proceed_step1,
            margin_top="4",
        ),
        spacing="6",
        align="start",
        padding="2.5em 2em",
        justify="center",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(16px)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="24px",
        width="100%",
        max_width="450px",
    )


# ── Steps 3/5: Transition Loading ─────────────────────────
def step_transition(title: str, subtitle: str) -> rx.Component:
    return rx.vstack(
        rx.spinner(size="3", color=NEUTRAL_WHITE),
        rx.heading(
            title,
            color=NEUTRAL_WHITE,
            font=FontSystem.SIZE_H2,
            margin_top="4",
        ),
        rx.text(
            subtitle,
            color="rgba(255,255,255,0.7)",
            font=FontSystem.SIZE_BODY,
        ),
        spacing="4",
        align="center",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(10px)",
        padding="3em",
        border_radius="1em",
    )


# ── Step 4: Profile Form ──────────────────────────────────
def step_profile() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Información personal",
            color=NEUTRAL_WHITE,
            font=FontSystem.SIZE_H2,
        ),
        rx.text(
            "Completa tu perfil para continuar",
            color="rgba(255,255,255,0.7)",
            font=FontSystem.SIZE_BODY,
            margin_bottom="4",
        ),
        rx.vstack(
            atom_input(
                placeholder="Nombre",
                value=AuthState.first_name,
                on_change=AuthState.set_first_name,
            ),
            atom_input(
                placeholder="Apellido",
                value=AuthState.last_name,
                on_change=AuthState.set_last_name,
            ),
            atom_input(
                placeholder="Fecha de nacimiento",
                type="date",
                value=AuthState.dob,
                on_change=AuthState.set_dob,
            ),
            width="100%",
            spacing="4",
        ),
        atom_button(
            "Finalizar",
            on_click=AuthState.submit_step3,
            disabled=(AuthState.first_name == "")
            | (AuthState.last_name == "")
            | (AuthState.dob == ""),
            margin_top="4",
        ),
        spacing="6",
        align="start",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(10px)",
        padding="3em",
        border_radius="1em",
        width="100%",
        max_width="450px",
    )
