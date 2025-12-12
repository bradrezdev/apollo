"""Componentes de layout - Banners y estructuras principales"""

import reflex as rx
from Proyecto_Apollo.styles import layout_styles


def desktop_banner() -> rx.Component:
    """Banner para vista desktop"""
    return rx.box(
        rx.image(
            src="/banner_web.jpg",
            **layout_styles.banner_desktop_style,
        ),
        **layout_styles.banner_container_desktop_style,
    )


def mobile_banner() -> rx.Component:
    """Banner para vista mobile"""
    return rx.container(
        rx.image(
            src="/banner_web.jpg",
            **layout_styles.banner_mobile_style,
        ),
        width="100%",
    )
