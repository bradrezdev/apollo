import typing
import reflex as rx
import asyncio
from datetime import datetime
from suplex import Suplex
from sqlmodel import select

from Proyecto_Apollo.components.ui import toast
from Proyecto_Apollo.models.users import Users


class AuthState(Suplex):
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

    def sign_up_user(self, email: str, password: str, first_name: str, last_name: str):
        """Registra usuario en Supabase Auth usando Suplex.
        
        IMPORTANTE: Suplex.sign_up() retorna el JSON de Supabase Auth pero
        NO guarda tokens automáticamente (a diferencia de sign_in_with_password).
        Por eso capturamos el UUID directamente del response, no de self.user_id.
        """
        try:
            email_clean = email.strip()
            password_clean = password.strip()
            
            # sign_up() retorna dict con datos del usuario
            result = self.sign_up(
                email=email_clean,
                password=password_clean,
                options={
                    "data": {
                        "first_name": first_name.strip(),
                        "last_name": last_name.strip()
                    }
                }
            )
            
            # Extraer UUID directamente del response de Supabase
            # El response puede tener el id en la raíz o dentro de "user"
            supabase_uid = None
            if isinstance(result, dict):
                supabase_uid = result.get("id")
                if not supabase_uid:
                    user_obj = result.get("user")
                    if isinstance(user_obj, dict):
                        supabase_uid = user_obj.get("id")
            
            print(f"[AUTH] Registro exitoso - email: {email_clean}, uid: {supabase_uid}")
            return True, "Usuario creado exitosamente", supabase_uid
        except Exception as e:
            error_msg = str(e).lower()
            print(f"[AUTH] Error en sign_up: {error_msg}")
            if "user already registered" in error_msg or "already been registered" in error_msg:
                return False, "El email ya está registrado", None
            elif "password" in error_msg:
                return False, "La contraseña no cumple con los requisitos", None
            elif "email" in error_msg:
                return False, "Email inválido", None
            return False, f"Error de registro: {str(e)}", None

    def sync_user_to_local_db(
        self,
        supabase_uid: str,
        email: str,
        first_name: str,
        last_name: str,
        dob: str,
    ) -> typing.Optional[int]:
        """Sincroniza el usuario de Supabase Auth con la tabla local 'users'.
        
        Patrón tomado de new-backoffice-onano:
        - Recibe TODOS los parámetros explícitamente (no depende de computed vars)
        - Busca por supabase_uid O email  
        - Si existe, actualiza. Si no, inserta.
        - Retorna el id local del usuario o None si falla.
        """
        if not supabase_uid:
            print(f"[SYNC] ERROR: supabase_uid es requerido")
            return None
        if not email:
            print(f"[SYNC] ERROR: email es requerido")
            return None
            
        print(f"[SYNC] Sincronizando: uid={supabase_uid}, email={email}")
        
        try:
            with rx.session() as session:
                # Buscar usuario existente por UID o email
                statement = select(Users).where(
                    (Users.supabase_uid == supabase_uid) | (Users.correo == email)
                )
                existing_user = session.exec(statement).first()
                
                if existing_user:
                    # UPDATE: actualizar datos
                    existing_user.supabase_uid = supabase_uid
                    existing_user.correo = email
                    existing_user.nombre = first_name
                    existing_user.apellido = last_name
                    existing_user.fecha_de_nacimiento = dob
                    session.add(existing_user)
                    session.commit()
                    print(f"[SYNC] Usuario ACTUALIZADO: id={existing_user.id}")
                    return existing_user.id
                else:
                    # INSERT: crear nuevo registro
                    new_user = Users(
                        supabase_uid=supabase_uid,
                        correo=email,
                        nombre=first_name,
                        apellido=last_name,
                        fecha_de_nacimiento=dob,
                        password_hash="supabase_managed",
                        salt="N/A",
                        bo_connection=False,
                    )
                    session.add(new_user)
                    session.commit()
                    session.refresh(new_user)
                    print(f"[SYNC] Usuario INSERTADO: id={new_user.id}, uid={new_user.supabase_uid}")
                    return new_user.id
        except Exception as e:
            print(f"[SYNC] ERROR al sincronizar: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def sign_in_user(self, email: str, password: str):
        """Inicia sesión en Supabase Auth usando Suplex."""
        try:
            email_clean = email.strip()
            password_clean = password.strip()
            self.sign_in_with_password(email=email_clean, password=password_clean)
            if self.user_is_authenticated:
                user_data = {
                    "id": self.user_id,
                    "email": self.user_email,
                    "first_name": self.user_metadata.get("first_name", "") if self.user_metadata else "",
                    "last_name": self.user_metadata.get("last_name", "") if self.user_metadata else "",
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
    def handle_logout(self):
        """Cierra sesión y redirige al inicio."""
        self.log_out()
        return rx.redirect("/")

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
                yield toast.error(error)
            return
        
        if self.can_proceed_step1:
            self.step = 3
            yield rx.call_script("if(window.animateParticleScroll){ window.animateParticleScroll(0.2, 800); }")
            await asyncio.sleep(2)
            self.step = 4

    @rx.event
    async def submit_login(self):
        """Intenta iniciar sesión con Supabase y sincroniza perfil local."""
        success, message, user_data = self.sign_in_user(self.email, self.password)
        
        if success:
            # Sincronizar usuario con tabla local (por si no existe aún)
            if user_data and user_data.get("id"):
                self.sync_user_to_local_db(
                    supabase_uid=user_data["id"],
                    email=user_data.get("email", self.email.strip()),
                    first_name=user_data.get("first_name", ""),
                    last_name=user_data.get("last_name", ""),
                    dob="N/A",
                )
            
            self.step = 3
            yield rx.call_script("if(window.animateParticleScroll){ window.animateParticleScroll(0.2, 800); }")
            await asyncio.sleep(2)
            yield rx.redirect("/chat")
        else:
            self.show_login_error = True

    @rx.event
    async def submit_step3(self):
        """Profile submitted → registro + auto-login + sync con tabla users."""
        # --- Validaciones ---
        if not self.first_name or not self.last_name or not self.dob:
            yield toast.error("Por favor completa todos los campos (nombre, apellido, fecha de nacimiento).")
            return
            
        try:
            dob_date = datetime.strptime(self.dob, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
            if age < 18:
                yield toast.error("Debes ser mayor de 18 años para registrarte.")
                return
        except ValueError:
            yield toast.error("Formato de fecha de nacimiento inválido.")
            return

        # --- PASO 1: Registrar en Supabase Auth ---
        # sign_up_user retorna (success, msg, supabase_uid)
        # El UID viene del response HTTP de Supabase, no de computed vars
        success, msg, supabase_uid = self.sign_up_user(
            self.email, self.password, self.first_name, self.last_name
        )
        
        if not success:
            yield toast.error(msg)
            return
        
        print(f"[AUTH] PASO 1 OK: Registro en Supabase Auth - uid={supabase_uid}")

        # --- PASO 2: Sincronizar con tabla users local ---
        # Hacemos esto ANTES del login porque ya tenemos el UID del response
        # Patrón del backoffice: pasar todos los datos explícitamente
        local_user_id = self.sync_user_to_local_db(
            supabase_uid=supabase_uid or "",
            email=self.email.strip(),
            first_name=self.first_name.strip(),
            last_name=self.last_name.strip(),
            dob=self.dob,
        )
        
        if local_user_id:
            print(f"[AUTH] PASO 2 OK: Usuario en tabla users - local_id={local_user_id}")
        else:
            print(f"[AUTH] PASO 2 WARN: sync_user_to_local_db retornó None")
            yield toast.error("Advertencia: No se pudo guardar el perfil localmente.")

        # --- PASO 3: Auto-login ---
        try:
            login_success, login_msg, user_data = self.sign_in_user(self.email, self.password)
            if not login_success:
                # Si el auto-login falla (ej: email confirmation requerido)
                yield toast.success("Registro exitoso. Revisa tu bandeja de entrada para confirmar tu correo e inicia sesión.")
                self.step = 0
                return
            print(f"[AUTH] PASO 3 OK: Auto-login exitoso")
        except Exception as e:
            print(f"[AUTH] PASO 3 ERROR: Auto-login falló: {e}")
            yield toast.success("Registro exitoso. Revisa tu bandeja de entrada para confirmar tu correo e inicia sesión.")
            self.step = 0
            return

        # --- PASO 4: Animación de carga y redirect ---
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

