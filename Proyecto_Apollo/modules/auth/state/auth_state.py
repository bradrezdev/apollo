import os
import typing
import reflex as rx
import asyncio
import httpx
from suplex import Suplex
from sqlmodel import select

from Proyecto_Apollo.components.ui import toast
from Proyecto_Apollo.models.users import Users

# Detectar entorno para uso en event handlers.
_is_dev = os.getenv("REFLEX_ENV", "dev").lower() in ("dev", "development", "local")


def _http_sign_up(api_url: str, api_key: str, email: str, password: str, redirect_to: str) -> dict:
    """Pure HTTP call to Supabase signup — no state access, safe for asyncio.to_thread."""
    url = f"{api_url}/auth/v1/signup"
    headers = {"apikey": api_key}
    data = {
        "email": email,
        "password": password,
        "email_redirect_to": redirect_to,
    }
    response = httpx.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def _http_sign_in(api_url: str, api_key: str, email: str, password: str) -> dict:
    """Pure HTTP call to Supabase signin — no state access, safe for asyncio.to_thread.

    Returns the full Supabase response dict including access_token, refresh_token, user.
    Raises httpx.HTTPStatusError on 400/401 etc.
    """
    url = f"{api_url}/auth/v1/token?grant_type=password"
    headers = {"apikey": api_key}
    data = {"email": email, "password": password}
    response = httpx.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


class AuthState(Suplex):
    """Estado para el flujo de autenticación y registro."""

    if typing.TYPE_CHECKING:
        set_email: typing.ClassVar[rx.EventHandler]
        set_password: typing.ClassVar[rx.EventHandler]
        set_confirm_password: typing.ClassVar[rx.EventHandler]
        set_first_name: typing.ClassVar[rx.EventHandler]
        set_last_name: typing.ClassVar[rx.EventHandler]
        set_terms_accepted: typing.ClassVar[rx.EventHandler]

    # ── Segment control ──────────────────────────────────
    # "registro" or "iniciar_sesion"
    segment: str = "registro"

    # ── Form fields ──────────────────────────────────────
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    terms_accepted: bool = False

    # Name form (post-login if user has no name)
    first_name: str = ""
    last_name: str = ""

    # ── UI state ─────────────────────────────────────────
    # NOTE: Cannot use `is_loading` — Suplex defines `is_loading = False` as a
    # plain class attribute (line 634 of suplex.py), which shadows the Reflex
    # field descriptor and makes the Var always resolve to a literal False.
    auth_loading: bool = False

    # Password visibility toggles
    show_password: bool = False
    show_confirm_password: bool = False

    # Post-login: show name form if user has no nombre
    show_name_form: bool = False

    # Loading animation step (0=not showing, 1/2/3=messages)
    loading_step: int = 0

    # ID del usuario en la tabla local 'users'
    local_user_id: int | None = None

    # Nombre para mostrar en la UI (cargado desde la BD local al iniciar sesión).
    # Declarado aquí (en AuthState) y no en DBState porque submit_login y submit_name
    # (ambos en AuthState) necesitan settearlo. Reflex no permite que una clase padre
    # setee un state var declarado en una clase hija.
    display_name: str = ""

    # Email para mostrar en la UI (cargado desde Users.correo en la BD local).
    # Suplex.user_email depende de JWT decode (JWKS/ES256) que puede fallar en dev.
    # Declarado aquí por la misma razón que display_name: submit_login (AuthState)
    # lo setea en la línea 435.
    display_email: str = ""

    # ── On Load ──────────────────────────────────────────
    def on_load(self):
        """Si ya tiene sesión activa, redirigir a /chat."""
        if self.access_token:
            return rx.redirect("/chat")

        self.segment = "registro"
        self.email = ""
        self.password = ""
        self.confirm_password = ""
        self.first_name = ""
        self.last_name = ""
        self.terms_accepted = False
        self.auth_loading = False
        self.show_name_form = False
        self.loading_step = 0
        self.show_password = False
        self.show_confirm_password = False
        # Reset particle state
        return rx.call_script(
            "window._apolloParticleProgress = 0;"
            "if(window.__oParticleHero){ window.__oParticleHero.setScrollProgress(0); }"
        )

    # ── Password visibility toggles ──────────────────────
    @rx.event
    def toggle_show_password(self):
        self.show_password = not self.show_password

    @rx.event
    def toggle_show_confirm_password(self):
        self.show_confirm_password = not self.show_confirm_password

    # ── Password validation computed vars ────────────────
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

    # ── Progressive reveal: show fields when @ detected ──
    @rx.var
    def show_extra_fields(self) -> bool:
        """Show password/extra fields when email contains @."""
        return "@" in self.email

    # ── Loading animation message ────────────────────────
    @rx.var
    def loading_message(self) -> str:
        if self.loading_step == 1:
            return "Cargando su información..."
        elif self.loading_step == 2:
            return "Cargando productos..."
        elif self.loading_step == 3:
            return "Cargando su asistente personal..."
        return ""

    # ── Helper: confirm URL ───────────────────────────────
    def _get_confirm_url(self) -> str:
        """Build the /confirm URL from the current host."""
        host = self.router.page.host  # e.g. "localhost:3000"
        protocol = "https" if "localhost" not in host else "http"
        return f"{protocol}://{host}/confirm"

    # ── Local DB sync ─────────────────────────────────────
    def sync_user_to_local_db(
        self,
        supabase_uid: str,
        email: str,
        first_name: str = "",
        last_name: str = "",
    ) -> typing.Optional[int]:
        """Sincroniza el usuario de Supabase Auth con la tabla local 'users'.

        Busca por supabase_uid O email. Si existe, actualiza. Si no, inserta.
        Retorna el id local del usuario o None.
        """
        if not supabase_uid:
            print("[SYNC] ERROR: supabase_uid es requerido")
            return None
        if not email:
            print("[SYNC] ERROR: email es requerido")
            return None

        print(f"[SYNC] Sincronizando: uid={supabase_uid}, email={email}")

        try:
            with rx.session() as session:
                statement = select(Users).where(
                    (Users.supabase_uid == supabase_uid) | (Users.correo == email)
                )
                existing_user = session.exec(statement).first()

                if existing_user:
                    existing_user.supabase_uid = supabase_uid
                    existing_user.correo = email
                    if first_name:
                        existing_user.nombre = first_name
                    if last_name:
                        existing_user.apellido = last_name
                    session.add(existing_user)
                    session.commit()
                    print(f"[SYNC] Usuario ACTUALIZADO: id={existing_user.id}")
                    return existing_user.id
                else:
                    new_user = Users(
                        supabase_uid=supabase_uid,
                        correo=email,
                        nombre=first_name,
                        apellido=last_name,
                        fecha_de_nacimiento="N/A",
                        password_hash="supabase_managed",
                        salt="N/A",
                        bo_connection=False,
                    )
                    session.add(new_user)
                    session.commit()
                    session.refresh(new_user)
                    print(f"[SYNC] Usuario INSERTADO: id={new_user.id}")
                    return new_user.id
        except Exception as e:
            print(f"[SYNC] ERROR al sincronizar: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _check_user_has_name(self, supabase_uid: str) -> bool:
        """Check if user has a first name in local DB."""
        try:
            with rx.session() as session:
                statement = select(Users).where(Users.supabase_uid == supabase_uid)
                user = session.exec(statement).first()
                if user and user.nombre and user.nombre.strip():
                    return True
                return False
        except Exception as e:
            print(f"[AUTH] Error checking user name: {e}")
            return False

    # ── Event handlers ───────────────────────────────────

    @rx.event
    def handle_logout(self):
        """Cierra sesión y redirige al inicio.

        Suplex.log_out() llama a POST /auth/v1/logout con el access_token actual.
        Supabase devuelve 403 si el token ya expiró (sesión inválida). En ese caso,
        igual limpiamos el estado local con self.reset() y redirigimos al inicio —
        el usuario ya no tiene una sesión válida de todas formas.
        """
        try:
            self.log_out()
        except Exception as e:
            # 403 / token expirado — la sesión ya no es válida en Supabase.
            # self.reset() resetea los Reflex state vars a sus defaults ("").
            # PERO las cookies del browser solo se borran si Reflex envía un
            # Set-Cookie con max_age=0. self.reset() no garantiza eso para
            # rx.Cookie fields — la cookie puede persistir y restaurarse en
            # el próximo page load. Por eso llamamos set_tokens("", "") después
            # del reset: fuerza que Reflex envíe Set-Cookie con valores vacíos.
            print(f"[AUTH] log_out falló ({type(e).__name__}: {e}) — limpiando estado local")
            self.reset()
            self.set_tokens(access_token="", refresh_token="")
        return rx.redirect("/")

    @rx.event
    async def submit_register(self):
        """Registro: valida campos, registra en Supabase (asyncio.to_thread), sincroniza local."""
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

        # Show loading spinner BEFORE network call
        self.auth_loading = True
        yield

        # Run blocking HTTP call off the event loop so the yield above is flushed
        email_clean = self.email.strip()
        password_clean = self.password.strip()
        confirm_url = self._get_confirm_url()

        try:
            result = await asyncio.to_thread(
                _http_sign_up,
                self._api_url,
                self._api_key,
                email_clean,
                password_clean,
                confirm_url,
            )
        except Exception as e:
            error_msg = str(e).lower()
            print(f"[AUTH] Error en sign_up: {error_msg}")
            self.auth_loading = False
            if "user already registered" in error_msg or "already been registered" in error_msg:
                yield toast.error("El email ya está registrado")
            elif "password" in error_msg:
                yield toast.error("La contraseña no cumple con los requisitos")
            elif "email" in error_msg:
                yield toast.error("Email inválido")
            else:
                yield toast.error("Error al registrar. Intenta de nuevo.")
            return

        # Extract UID from response
        supabase_uid = None
        if isinstance(result, dict):
            supabase_uid = result.get("id")
            if not supabase_uid:
                user_obj = result.get("user")
                if isinstance(user_obj, dict):
                    supabase_uid = user_obj.get("id")

        print(f"[AUTH] Registro exitoso - email: {email_clean}, uid: {supabase_uid}")

        # Sync to local DB (without name, just email + uid)
        local_user_id = self.sync_user_to_local_db(
            supabase_uid=supabase_uid or "",
            email=email_clean,
        )
        if local_user_id:
            self.local_user_id = local_user_id
            print(f"[AUTH] Usuario sincronizado - local_id={local_user_id}")

        self.auth_loading = False

        # Show success toast and switch to login segment
        yield toast.success(
            "Registro exitoso. Revisa tu bandeja de entrada para confirmar tu correo electrónico."
        )

        # Clear form and switch to login
        self.email = ""
        self.password = ""
        self.confirm_password = ""
        self.terms_accepted = False
        self.segment = "iniciar_sesion"

    @rx.event
    async def submit_login(self):
        """Login: valida, autentica (asyncio.to_thread), checa nombre -> /chat o name form."""
        if not self.email or not self.is_email_valid:
            yield toast.error("Ingresa un correo electrónico válido")
            return
        if not self.password:
            yield toast.error("Ingresa tu contraseña")
            return

        # Show loading spinner BEFORE network call
        self.auth_loading = True
        yield

        # Run blocking HTTP call off the event loop
        email_clean = self.email.strip()
        password_clean = self.password.strip()

        try:
            result = await asyncio.to_thread(
                _http_sign_in,
                self._api_url,
                self._api_key,
                email_clean,
                password_clean,
            )
        except Exception as e:
            error_msg = str(e).lower()
            print(f"[AUTH] Error en sign_in: {error_msg}")
            self.auth_loading = False
            if "email not confirmed" in error_msg:
                yield toast.error("Por favor confirma tu email antes de iniciar sesión")
            else:
                yield toast.error(
                    "Correo electrónico y/o Contraseña no coinciden con nuestros registros"
                )
            return

        # Extract tokens and user data from response
        access_token = result.get("access_token", "")
        refresh_token = result.get("refresh_token", "")
        user_obj = result.get("user") or {}
        supabase_uid = user_obj.get("id") or result.get("id", "")
        user_email = user_obj.get("email", email_clean)
        meta = user_obj.get("user_metadata") or {}
        first_name = meta.get("first_name", "")
        last_name = meta.get("last_name", "")

        if not supabase_uid:
            self.auth_loading = False
            yield toast.error(
                "Correo electrónico y/o Contraseña no coinciden con nuestros registros"
            )
            return

        # Set tokens on main state (must be done here, not in thread)
        self.set_tokens(access_token=access_token, refresh_token=refresh_token)
        print(f"[AUTH] Login exitoso - uid={supabase_uid}, email={user_email}")
        # Flush cookie mutations to browser BEFORE redirect. Without this yield,
        # Reflex batches the cookie-set and rx.redirect() in the same delta update,
        # causing the browser to navigate to /chat before it has stored the cookies.
        # State.on_load then sees empty tokens and immediately redirects back to /.
        yield

        # Sync user to local DB
        local_id = self.sync_user_to_local_db(
            supabase_uid=supabase_uid,
            email=user_email,
            first_name=first_name,
            last_name=last_name,
        )
        if local_id:
            self.local_user_id = local_id

        # Cache email for display (Suplex.user_email depends on JWT/JWKS decode which
        # can fail with ES256 + placeholder jwt_secret; this guarantees email is shown)
        if user_email:
            self.display_email = user_email

        self.auth_loading = False

        # Check if user has a name in local DB
        has_name = self._check_user_has_name(supabase_uid)

        if has_name:
            yield rx.redirect("/chat")
        else:
            self.show_name_form = True

    @rx.event
    async def submit_name(self):
        """Save name/apellido, then run loading animation -> redirect to /chat."""
        if not self.first_name.strip():
            yield toast.error("El nombre es requerido")
            return
        if not self.last_name.strip():
            yield toast.error("El apellido es requerido")
            return

        self.auth_loading = True
        yield

        # Update user name in local DB
        try:
            supabase_uid = None
            if isinstance(self.user_id, str) and self.user_id:
                supabase_uid = self.user_id

            # Also try to get it from local_user_id lookup
            if not supabase_uid and self.local_user_id:
                with rx.session() as session:
                    user = session.get(Users, self.local_user_id)
                    if user:
                        supabase_uid = user.supabase_uid

            if supabase_uid:
                with rx.session() as session:
                    statement = select(Users).where(Users.supabase_uid == supabase_uid)
                    user = session.exec(statement).first()
                    if user:
                        user.nombre = self.first_name.strip()
                        user.apellido = self.last_name.strip()
                        session.add(user)
                        session.commit()
                        print(f"[AUTH] Nombre actualizado: {self.first_name} {self.last_name}")
            elif self.local_user_id:
                with rx.session() as session:
                    user = session.get(Users, self.local_user_id)
                    if user:
                        user.nombre = self.first_name.strip()
                        user.apellido = self.last_name.strip()
                        session.add(user)
                        session.commit()
                        print(
                            f"[AUTH] Nombre actualizado via local_id: "
                            f"{self.first_name} {self.last_name}"
                        )
        except Exception as e:
            print(f"[AUTH] Error updating name: {e}")

        # Actualizar display_name en el estado para reflejarlo inmediatamente en la UI
        full_name = f"{self.first_name.strip()} {self.last_name.strip()}".strip()
        if full_name:
            self.display_name = full_name

        self.auth_loading = False
        self.show_name_form = False

        # Loading animation sequence
        self.loading_step = 1
        yield
        await asyncio.sleep(2)

        self.loading_step = 2
        yield
        await asyncio.sleep(2)

        self.loading_step = 3
        yield
        await asyncio.sleep(2)

        self.loading_step = 0
        yield rx.redirect("/chat")
