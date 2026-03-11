import typing
import reflex as rx
import asyncio
from suplex import Suplex


class ConfirmState(Suplex):
    """Estado para la página de confirmación de cuenta."""

    is_confirmed: bool = False
    is_loading: bool = True
    error_message: str = ""
    countdown: int = 5

    def on_load(self, token_hash: str = "", type: str = ""):
        """Valida el token de confirmación y muestra el resultado."""
        self.is_loading = True
        self.error_message = ""

        if not token_hash:
            self.error_message = "Token de confirmación inválido"
            self.is_loading = False
            return

        try:
            result = self.verify_otp(token_hash=token_hash, otp_type=type or "signup")
            
            if result and isinstance(result, dict):
                if result.get("user") or result.get("id"):
                    self.is_confirmed = True
                    print(f"[CONFIRM] Cuenta confirmada exitosamente")
                else:
                    self.error_message = "Token de confirmación inválido o expirado"
            else:
                self.error_message = "No se pudo confirmar la cuenta"
                
        except Exception as e:
            error_msg = str(e).lower()
            print(f"[CONFIRM] Error: {error_msg}")
            
            if "invalid" in error_msg or "expired" in error_msg:
                self.error_message = "El enlace de confirmación ha expirado o ya fue usado"
            else:
                self.error_message = "Error al confirmar la cuenta"
        
        self.is_loading = False

    @rx.event
    async def start_countdown(self):
        """Inicia el conteo regresivo de 5 segundos."""
        for i in range(5, 0, -1):
            self.countdown = i
            yield
            await asyncio.sleep(1)
        yield rx.redirect("/")

    @rx.event
    def go_to_login(self):
        """Redirige manualmente al login."""
        return rx.redirect("/")
