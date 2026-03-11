import reflex as rx
from ...styles.colors import *
from ...styles import fonts
from typing import Any

def button(
    text: str | rx.Component,
    on_click: Any = None,
    variant: str = "primary",
    width="100%",
    loading: Any = False,
    disabled: Any = False,
    **kwargs,
) -> rx.Component:
    """Botón atómico reutilizable que sigue el Design System.

    Props como `loading` y `disabled` se pasan directamente a rx.button
    (no como parte del dict de estilos).
    """
    # Base styling
    base_style = {
        "height": "48px",
        "width": width,
        "border_radius": "24px",
        "font_family": fonts.FONT_FAMILY_PRIMARY,
        "font_size": fonts.SIZE_H3,
        "font_weight": fonts.WEIGHT_SEMIBOLD,
        "cursor": "pointer",
        "transition": "all 0.2s ease-in-out",
        "_hover": {"transform": "scale(1.02)"}
    }

    if variant == "primary":
        base_style.update({
            "bg": rx.color_mode_cond(
                light=BRAND_SECONDARY_100,
                dark=BRAND_SECONDARY_100
            ),
            "color": rx.color_mode_cond(
                light=BRAND_WHITE,
                dark=BRAND_WHITE
            ),
            "border": "none",
        })
    elif variant == "outline":
        base_style.update({
            "bg": "transparent",
            "color": rx.color_mode_cond(
                light=BRAND_SECONDARY_100,
                dark=BRAND_WHITE
            ),
            "border": f"2px solid {BRAND_SECONDARY_100}",
        })
    elif variant == "ghost":
        base_style.update({
            "bg": "transparent",
            "color": rx.color_mode_cond(
                light=BRAND_PRIMARY_100,
                dark=BRAND_SECONDARY_100
            ),
            "border": "none",
            "opacity": "0.8",
            "_hover": {"opacity": "1.0", "bg": "rgba(255,255,255,0.1)"}
        })

    # Remaining kwargs are style overrides (e.g. margin_top, padding).
    # loading / disabled are rx.button props — must NOT be in the style dict.
    return rx.button(
        text,
        on_click=on_click,
        loading=loading,
        disabled=disabled,
        **{**base_style, **kwargs},
    )
