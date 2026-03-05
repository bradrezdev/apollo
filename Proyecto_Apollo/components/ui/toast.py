import reflex as rx
from ...styles.colors import *
from ...styles import fonts

from typing import Any

class CustomToastWrapper:
    """Wrapper para crear eventos de toast con opciones personalizables."""
    
    def _create_toast(
        self,
        message: str | rx.Var[str],
        type_name: str | None = None,
        close_button: bool = True,
        # Se asignará bg_color y color dinámicamente según light/dark mode
        bg_color: str | rx.Var[str] | None = None,
        color: str | rx.Var[str] | None = None,
        position: str = "top-right",
        duration: int = 5000,
        width: str = "fit-content",
        **kwargs
    ) -> rx.event.EventSpec:
        
        # Estilos base para todos los toasts
        style: dict[str, Any] = {
            "font_family": "var(--font-family)",  # Usar tipografía global
            "border_radius": "32px",
            "box_shadow": "0px 4px 12px rgba(0, 0, 0, 0.15)",
            "width": width,
        }
        
        # Si es el toast custom general, asignamos un color base si no trae
        if type_name is None and bg_color is None:
            bg_color = rx.color_mode_cond(light=BRAND_PRIMARY_100, dark=BRAND_SECONDARY_100)
            
        # Si hay bg_color o color definido, lo inyectamos
        if bg_color is not None:
            style["background-color"] = bg_color
        if color is not None:
            style["color"] = color

        if "style" in kwargs:
            style.update(kwargs.pop("style"))

        # Seleccionamos el método correcto de rx.toast
        toast_func = getattr(rx.toast, type_name) if type_name else rx.toast

        return toast_func(
            message,
            close_button=close_button,
            position=position,
            duration=duration,
            style=style,
            **kwargs
        )

    def __call__(
        self, 
        message: str | rx.Var[str], 
        bg_color: str | rx.Var[str] | None = None, 
        color: str | rx.Var[str] | None = None, 
        close_button: bool = True, 
        **kwargs
    ):
        """Toast personalizable en su totalidad."""
        return self._create_toast(message, None, close_button, bg_color, color, **kwargs)

    def success(self, message: str | rx.Var[str], close_button: bool = True, **kwargs):
        """Toast de éxito."""
        return self._create_toast(message, "success", close_button, None, color="#2e7d32", **kwargs)

    def error(self, message: str | rx.Var[str], close_button: bool = True, **kwargs):
        """Toast de error."""
        return self._create_toast(message, "error", close_button, None, color="#2D0607", **kwargs)

    def warning(self, message: str | rx.Var[str], close_button: bool = True, **kwargs):
        """Toast de advertencia."""
        return self._create_toast(message, "warning", close_button, None, color="#ed6c02", **kwargs)

    def info(self, message: str | rx.Var[str], close_button: bool = True, **kwargs):
        """Toast informativo."""
        return self._create_toast(message, "info", close_button, None, color="#0288d1", **kwargs)

# Instancia exportada para ser usada como el átomo 'toast'
toast = CustomToastWrapper()