import reflex as rx

# Importar componentes modulares
from ..components.chat_components import responsive_chat_container
from ..components.sidebar_components import desktop_sidebar, edit_conversation_dialog, delete_conversation_dialog
from ...core.components.splash_screen import splash_screen
from ..components.header_components import mobile_header
from ..state.chat_state import State
from Proyecto_Apollo.components.ui import user_profile_drawer

def unified_view() -> rx.Component:
    """Vista unificada y responsiva para todos los dispositivos"""
    return rx.flex(
        # Mobile header — absolute dentro del contenedor fixed para anclarse al --app-height
        rx.box(
            mobile_header(),
            display=["block", "block", "none", "none"],
            position="absolute",
            top="0",
            left="0",
            width="100%",
            z_index="1000",
        ),
        
        desktop_sidebar(),
        
        rx.box(
            responsive_chat_container(),
            flex="1",
            width="100%",
            height="100%",
            position="relative",
            overflow="hidden",
        ),
        
        width="100%",
        height="var(--app-height, 100dvh)",
        flex_direction="row",
        align_items="stretch",
        overflow="hidden",
        position="fixed",
        top="0",
        left="0",
    )

def chat_page() -> rx.Component:
    """Punto de entrada principal - Renderiza vista unificada"""
    return rx.box(
        # Script para bloquear scroll global en iOS y ajustar altura al teclado
        rx.script("""
            // === 1. Bloquear touchmove fuera del chat ===
            document.addEventListener('touchmove', function(e) {
                let node = e.target;
                while (node && node !== document.body) {
                    if (node.classList && node.classList.contains('chat-scroll-area')) {
                        return;
                    }
                    node = node.parentNode;
                }
                e.preventDefault();
            }, { passive: false });

            // === 2. Ajustar --app-height con visualViewport ===
            function setAppHeight() {
                var vh = window.visualViewport ? window.visualViewport.height : window.innerHeight;
                document.documentElement.style.setProperty('--app-height', vh + 'px');
            }
            setAppHeight();
            if (window.visualViewport) {
                window.visualViewport.addEventListener('resize', setAppHeight);
                window.visualViewport.addEventListener('scroll', function() {
                    // Forzar scroll del viewport a 0 para evitar que iOS mueva la página
                    window.scrollTo(0, 0);
                });
            }
            window.addEventListener('resize', setAppHeight);
        """),
        splash_screen(),
        unified_view(),
        edit_conversation_dialog(),
        delete_conversation_dialog(),
        user_profile_drawer(
            user_name=State.user_name,
            user_email=State.user_email,
            is_open=State.is_profile_drawer_open,
            on_open_change=State.set_profile_drawer_open,
            on_logout=State.handle_logout,
        ),
        height="var(--app-height, 100dvh)",
        overflow="hidden",
    )
