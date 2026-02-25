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
        
    step: int = 0
    
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    terms_accepted: bool = False
    
    first_name: str = ""
    last_name: str = ""
    dob: str = ""
    
    final_message: str = "Preparando tu asistente personal"
    
    def on_load(self):
        self.step = 0
        self.email = ""
        self.password = ""
        self.confirm_password = ""
        self.first_name = ""
        self.last_name = ""
        self.dob = ""
        self.terms_accepted = False
        return rx.call_script("if(typeof initParticleHero === 'function' && !window.onanoParticleSim){ window.onanoParticleSim = initParticleHero('particle-hero-canvas'); } if(window.onanoParticleSim){ window.onanoParticleSim.setScrollProgress(0); }")

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
            self.has_lowercase and 
            self.has_uppercase and 
            self.has_number and 
            self.has_special and 
            len(self.password) >= 8
        )
        
    @rx.var
    def passwords_match(self) -> bool:
        return self.password == self.confirm_password and len(self.password) > 0
        
    @rx.var
    def is_email_valid(self) -> bool:
        return "@" in self.email and "." in self.email.split("@")[-1]
        
    @rx.var
    def can_proceed_step1(self) -> bool:
        return self.is_email_valid and self.is_password_valid and self.passwords_match and self.terms_accepted

    @rx.event
    def go_to_register(self):
        self.step = 1
        return rx.call_script("if(window.onanoParticleSim){ window.onanoParticleSim.setScrollProgress(0.5); }")
        
    @rx.event
    def go_to_login(self):
        return rx.call_script("if(window.onanoParticleSim){ window.onanoParticleSim.setScrollProgress(0.5); }")
        
    @rx.event
    def go_back(self):
        self.step = 0
        return rx.call_script("if(window.onanoParticleSim){ window.onanoParticleSim.setScrollProgress(0.0); }")
        
    @rx.event
    async def submit_step1(self):
        if self.can_proceed_step1:
            self.step = 2
            yield rx.call_script("if(window.onanoParticleSim){ window.onanoParticleSim.setScrollProgress(0.2); }")
            await asyncio.sleep(2)
            self.step = 3
            
    @rx.event
    async def submit_step3(self):
        if self.first_name and self.last_name and self.dob:
            self.step = 4
            self.final_message = "Cargando productos..."
            yield rx.call_script("if(window.onanoParticleSim){ window.onanoParticleSim.setScrollProgress(0.5); }")
            yield
            
            await asyncio.sleep(2)
            self.final_message = "Cargando plan de compensación..."
            yield rx.call_script("if(window.onanoParticleSim){ window.onanoParticleSim.setScrollProgress(0.8); }")
            yield
            
            await asyncio.sleep(2)
            self.final_message = "Cargando tu asistente personal..."
            yield rx.call_script("if(window.onanoParticleSim){ window.onanoParticleSim.setScrollProgress(1.0); }")
            yield
            
            await asyncio.sleep(2)
            yield rx.redirect("/chat")

def auth_page_ui() -> rx.Component:
    return rx.box(
        rx.el.canvas(
            id="particle-hero-canvas",
            style={
                "display": "block",
                "width": "100%",
                "height": "100%",
                "position": "fixed",
                "top": "0",
                "left": "0",
                "z_index": "-1"
            },
        ),
        rx.script(src="/scripts/particle_hero.js"),
        rx.script("window.addEventListener('load', () => { if(typeof initParticleHero === 'function'){ window.onanoParticleSim = initParticleHero('particle-hero-canvas'); }});"),
        
        rx.center(
            rx.match(
                AuthState.step,
                (0, step_initial()),
                (1, step_register()),
                (2, step_transition("Creando nueva cuenta", "Ya casi terminamos con tu registro")),
                (3, step_profile()),
                (4, step_transition("Preparando tu asistente personal", AuthState.final_message)),
                step_initial()
            ),
            width="100%",
            height="100vh",
            position="relative",
            z_index="1"
        )
    )

def step_initial() -> rx.Component:
    return rx.vstack(
        rx.image(src="/dark-logo.svg", height="6em", margin_bottom="2em"),
        rx.heading("Bienvenido a Apollo", color=NEUTRAL_WHITE, font=FontSystem.SIZE_H2),
        rx.text("Tu asistente personal potenciado por la nanotecnología de ONANO®", color=NEUTRAL_WHITE, font=FontSystem.SIZE_BODY, margin_bottom="1em"),
        rx.vstack(
            atom_button("Iniciar sesión", on_click=AuthState.go_to_login, variant="outline"),
            atom_button("Registrarse", on_click=AuthState.go_to_register, variant="primary"),
            spacing="4",
            width="100%"
        ),
        padding="0 10px",
        justify="center",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(16px)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        height="120vh",
        width="100%",
        max_width="400px"
    )

def step_register() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            atom_button(
                rx.icon("chevron-left", size=24), 
                on_click=AuthState.go_back, 
                variant="ghost", 
                width="auto", 
                padding="0.5em",
                border_radius="50%"
            ),
            rx.heading("Crear cuenta", color=NEUTRAL_WHITE, font=FontSystem.SIZE_H2),
            align="center",
            width="100%",
            spacing="2"
        ),
        rx.vstack(
            atom_input(placeholder="Correo electrónico", type="email", value=AuthState.email, on_change=AuthState.set_email),
            atom_input(placeholder="Contraseña", type="password", value=AuthState.password, on_change=AuthState.set_password),
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
                spacing="2"
            ),
            atom_input(placeholder="Confirmar contraseña", type="password", value=AuthState.confirm_password, on_change=AuthState.set_confirm_password),
            rx.checkbox(
                "Acepto los Términos y Condiciones, autorizando el tratamiento de mis datos personales de acuerdo a la normativa legal vigente para el uso de esta plataforma.",
                checked=AuthState.terms_accepted,
                on_change=AuthState.set_terms_accepted,
                color="rgba(255,255,255,0.8)",
                font_size=FontSystem.SIZE_MICRO,
                font_family=FontSystem.SECONDARY_FONT
            ),
            width="100%",
            spacing="4"
        ),
        atom_button("Siguiente", on_click=AuthState.submit_step1, disabled=~AuthState.can_proceed_step1, margin_top="4"),
        spacing="6",
        align="start",
        padding="2.5em 2em",
        justify="center",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(16px)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="24px",
        width="100%",
        max_width="450px"
    )

def step_transition(title: str, subtitle: str) -> rx.Component:
    return rx.vstack(
        rx.spinner(size="3", color=NEUTRAL_WHITE),
        rx.heading(title, color=NEUTRAL_WHITE, font=FontSystem.SIZE_H2, margin_top="4"),
        rx.text(subtitle, color="rgba(255,255,255,0.7)", font=FontSystem.SIZE_BODY),
        spacing="4",
        align="center",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(10px)",
        padding="3em",
        border_radius="1em"
    )

def step_profile() -> rx.Component:
    return rx.vstack(
        rx.heading("Información personal", color=NEUTRAL_WHITE, font=FontSystem.SIZE_H2),
        rx.text("Completa tu perfil para continuar", color="rgba(255,255,255,0.7)", font=FontSystem.SIZE_BODY, margin_bottom="4"),
        rx.vstack(
            atom_input(placeholder="Nombre", value=AuthState.first_name, on_change=AuthState.set_first_name),
            atom_input(placeholder="Apellido", value=AuthState.last_name, on_change=AuthState.set_last_name),
            atom_input(placeholder="Fecha de nacimiento", type="date", value=AuthState.dob, on_change=AuthState.set_dob),
            width="100%",
            spacing="4"
        ),
        atom_button(
            "Finalizar", 
            on_click=AuthState.submit_step3, 
            disabled=(AuthState.first_name == "") | (AuthState.last_name == "") | (AuthState.dob == ""),
            margin_top="4"
        ),
        spacing="6",
        align="start",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(10px)",
        padding="3em",
        border_radius="1em",
        width="100%",
        max_width="450px"
    )
