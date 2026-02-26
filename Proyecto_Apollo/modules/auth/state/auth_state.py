import typing
import reflex as rx
import asyncio

from Proyecto_Apollo.modules.auth.backend.supabase_client import supabase

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

    show_login_error: bool = False

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
        self.show_login_error = False
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

    async def sign_up_user(self, email: str, password: str, first_name: str, last_name: str):
        """Registra usuario en Supabase Auth."""
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "first_name": first_name,
                        "last_name": last_name
                    }
                }
            })
            
            if response.user:
                return True, "Usuario creado exitosamente", response.user.id
            else:
                return False, "Error creando usuario en Supabase", None
                
        except Exception as e:
            error_msg = str(e).lower()
            
            if "user already registered" in error_msg or "already been registered" in error_msg:
                return False, "El email ya está registrado", None
            elif "password" in error_msg:
                return False, "La contraseña no cumple con los requisitos", None
            elif "email" in error_msg:
                return False, "Email inválido", None
            
            return False, f"Error de registro: {str(e)}", None

    async def sign_in_user(self, email: str, password: str):
        """Inicia sesión en Supabase Auth."""
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                user_data = {
                    "id": response.user.id,
                    "email": response.user.email,
                    "first_name": response.user.user_metadata.get("first_name", ""),
                    "last_name": response.user.user_metadata.get("last_name", ""),
                    "access_token": response.session.access_token if response.session else None,
                }
                return True, "Login exitoso", user_data
            else:
                return False, "Credenciales inválidas", None
                
        except Exception as e:
            error_msg = str(e).lower()
            
            if "invalid login credentials" in error_msg or "invalid" in error_msg:
                return False, "Email o contraseña incorrectos", None
            elif "email not confirmed" in error_msg:
                return False, "Por favor confirma tu email antes de iniciar sesión", None
            
            return False, f"Error de login: {str(e)}", None

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
        return rx.call_script(
            "if(window.animateParticleScroll){ window.animateParticleScroll(0.5, 800); }"
        )

    @rx.event
    def go_to_login(self):
        """Welcome → Login (slide left). Particles: disperse to 0.5."""
        self.step = 0
        return rx.call_script(
            "if(window.animateParticleScroll){ window.animateParticleScroll(0.5, 800); }"
        )

    @rx.event
    def close_login_error(self):
        """Cierra el dialog de error de login."""
        self.show_login_error = False

    @rx.event
    def go_back(self):
        """Any form → Welcome (slide back). Particles: re-agglomerate to 0."""
        self.step = 1
        return rx.call_script(
            "if(window.animateParticleScroll){ window.animateParticleScroll(0.0, 800); }"
        )

    @rx.event
    async def submit_step1(self):
        """Register form submitted → transition → profile."""
        validation_errors = []
        
        if not self.email:
            validation_errors.append("El correo electrónico es requerido")
        elif not self.is_email_valid:
            validation_errors.append("El correo electrónico no es válido")
            
        if not self.password:
            validation_errors.append("La contraseña es requerida")
        elif not self.is_password_valid:
            validation_errors.append("La contraseña no cumple con los requisitos")
            
        if not self.confirm_password:
            validation_errors.append("Debes confirmar tu contraseña")
        elif not self.passwords_match:
            validation_errors.append("Las contraseñas no coinciden")
            
        if not self.terms_accepted:
            validation_errors.append("Debes aceptar los términos y condiciones")
        
        if validation_errors:
            for error in validation_errors:
                yield rx.toast(
                    error,
                    style={
                        "font_style": fonts.STYLE_LABEL,
                        "background-color": BRAND_ERROR,
                        "color": BRAND_ERROR_LIGHT,
                        "border-radius": "32px",

                    },
                    close_button=True,
                    duration=7000,
                    position="top"
                )
            return
        
        if self.can_proceed_step1:
            self.step = 3
            yield rx.call_script("if(window.animateParticleScroll){ window.animateParticleScroll(0.2, 800); }")
            await asyncio.sleep(2)
            self.step = 4

    @rx.event
    async def submit_login(self):
        """Intenta iniciar sesión con Supabase."""
        success, message, user_data = await self.sign_in_user(self.email, self.password)
        
        if success:
            self.step = 3
            yield rx.call_script("if(window.animateParticleScroll){ window.animateParticleScroll(0.2, 800); }")
            await asyncio.sleep(2)
            self.step = 4
        else:
            self.show_login_error = True

    @rx.event
    async def submit_step3(self):
        """Profile submitted → final loading sequence."""
        if self.first_name and self.last_name and self.dob:
            self.step = 5
            self.final_message = "Cargando productos..."
            yield rx.call_script("if(window.animateParticleScroll){ window.animateParticleScroll(0.5, 1200); }")
            yield
            await asyncio.sleep(2)

            self.final_message = "Cargando plan de compensación..."
            yield rx.call_script("if(window.animateParticleScroll){ window.animateParticleScroll(0.8, 1200); }")
            yield
            await asyncio.sleep(2)

            self.final_message = "Cargando tu asistente personal..."
            yield rx.call_script("if(window.animateParticleScroll){ window.animateParticleScroll(1.0, 1200); }")
            yield
            await asyncio.sleep(2)

            yield rx.redirect("/chat")


# ═══════════════════════════════════════════════════════════
#  UI COMPONENTS
# ═══════════════════════════════════════════════════════════

