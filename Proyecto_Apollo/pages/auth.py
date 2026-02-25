import reflex as rx
import asyncio

class AuthState(rx.State):
    """Estado para el flujo de autenticación y registro."""
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

    def go_to_register(self):
        self.step = 1
        
    def go_to_login(self):
        pass
        
    async def submit_step1(self):
        if self.can_proceed_step1:
            self.step = 2
            yield rx.call_script("if(window.onanoParticleSim){ window.onanoParticleSim.setScrollProgress(0.2); }")
            await asyncio.sleep(2)
            self.step = 3
            
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
        rx.image(src="/isologo-light.svg", height="4em", margin_bottom="1em"),
        rx.heading("Bienvenido a Apollo", color="white", size="9"),
        rx.text("Tu asistente personal potenciado con IA", color="rgba(255,255,255,0.7)", size="4", margin_bottom="1em"),
        rx.vstack(
            rx.button("Iniciar sesión", on_click=AuthState.go_to_login, size="4", width="100%", variant="surface", color_scheme="blue", border_radius="full"),
            rx.button("Registrarse", on_click=AuthState.go_to_register, size="4", width="100%", color_scheme="blue", border_radius="full"),
            spacing="4",
            width="100%"
        ),
        spacing="4",
        align="center",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(16px)",
        padding="3em",
        border_radius="2em",
        border="1px solid rgba(255, 255, 255, 0.1)",
        width="100%",
        max_width="400px"
    )

def _validation_rule(label: str, is_valid: rx.Var[bool]) -> rx.Component:
    return rx.hstack(
        rx.cond(
            is_valid,
            rx.icon("circle-check", color="green", size=16),
            rx.icon("circle-x", color="gray", size=16)
        ),
        rx.cond(
            is_valid,
            rx.text(label, color="green", size="2"),
            rx.text(label, color="gray", size="2")
        ),
        spacing="2",
        align="center"
    )

def step_register() -> rx.Component:
    return rx.vstack(
        rx.heading("Crear cuenta", color="white", size="8"),
        rx.vstack(
            rx.input(placeholder="Correo electrónico", type="email", value=AuthState.email, on_change=AuthState.set_email, size="3", width="100%", radius="full"),
            rx.input(placeholder="Contraseña", type="password", value=AuthState.password, on_change=AuthState.set_password, size="3", width="100%", radius="full"),
            rx.box(
                _validation_rule("Una letra minúscula", AuthState.has_lowercase),
                _validation_rule("Una letra mayúscula", AuthState.has_uppercase),
                _validation_rule("Un número", AuthState.has_number),
                _validation_rule("Un símbolo especial", AuthState.has_special),
                _validation_rule("Mínimo 8 caracteres", AuthState.is_length_valid),
                margin_y="4",
                padding="1em",
                background="rgba(255,255,255,0.05)",
                border_radius="1em"
            ),
            rx.input(placeholder="Confirmar contraseña", type="password", value=AuthState.confirm_password, on_change=AuthState.set_confirm_password, size="3", width="100%", radius="full"),
            rx.checkbox(
                "Acepto los Términos y Condiciones, autorizando el tratamiento de mis datos personales de acuerdo a la normativa legal vigente para el uso de esta plataforma.",
                checked=AuthState.terms_accepted,
                on_change=AuthState.set_terms_accepted,
                color="white",
                size="2"
            ),
            width="100%",
            spacing="4"
        ),
        rx.button("Siguiente", on_click=AuthState.submit_step1, disabled=~AuthState.can_proceed_step1, size="4", width="100%", color_scheme="blue", margin_top="4", border_radius="full"),
        spacing="6",
        align="start",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(10px)",
        padding="3em",
        border_radius="1em",
        width="100%",
        max_width="450px"
    )

def step_transition(title: str, subtitle: str) -> rx.Component:
    return rx.vstack(
        rx.spinner(size="3", color="white"),
        rx.heading(title, color="white", size="7", margin_top="4"),
        rx.text(subtitle, color="rgba(255,255,255,0.7)", size="4"),
        spacing="4",
        align="center",
        background="rgba(6, 42, 99, 0.4)",
        backdrop_filter="blur(10px)",
        padding="3em",
        border_radius="1em"
    )

def step_profile() -> rx.Component:
    return rx.vstack(
        rx.heading("Información personal", color="white", size="8"),
        rx.text("Completa tu perfil para continuar", color="rgba(255,255,255,0.7)", margin_bottom="4"),
        rx.vstack(
            rx.input(placeholder="Nombre", value=AuthState.first_name, on_change=AuthState.set_first_name, size="3", width="100%", radius="full"),
            rx.input(placeholder="Apellido", value=AuthState.last_name, on_change=AuthState.set_last_name, size="3", width="100%", radius="full"),
            rx.input(placeholder="Fecha de nacimiento", type="date", value=AuthState.dob, on_change=AuthState.set_dob, size="3", width="100%", radius="full"),
            width="100%",
            spacing="4"
        ),
        rx.button(
            "Finalizar", 
            on_click=AuthState.submit_step3, 
            disabled=(AuthState.first_name == "") | (AuthState.last_name == "") | (AuthState.dob == ""),
            size="4", width="100%", color_scheme="blue", margin_top="4", border_radius="full"
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
