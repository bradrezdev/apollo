import reflex as rx
from Proyecto_Apollo.components.ui import button, input, badge, toast, alert_dialog, dialog

class TestingAtomsState(rx.State):
    """Estado para la página de testing de átomos."""
    test_value: str = ""
    is_valid: bool = False
    
    def validate_input(self, value: str):
        self.test_value = value
        self.is_valid = len(value) > 3
        
    def show_toast(self):
        return toast.success("Esto es un Toast de prueba desde el state", position="bottom-right")

def testing_atoms_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Página de Testing - Átomos UI", size="8", margin_bottom="20px"),
            rx.text("Aquí se encuentran todos los componentes 'átomo' para editar su estilo base y que se replique en todo el proyecto."),
            
            rx.divider(margin_y="20px"),
            
            rx.heading("Botones", size="6", margin_bottom="10px"),
            rx.hstack(
                button("Primary Button", variant="primary", width="200px"),
                button("Outline Button", variant="outline", width="200px"),
                button("Ghost Button", variant="ghost", width="200px"),
                spacing="4"
            ),
            
            rx.divider(margin_y="20px"),
            
            rx.heading("Inputs", size="6", margin_bottom="10px"),
            rx.vstack(
                input(
                    placeholder="Escribe algo (>3 chars para validar)", 
                    value=TestingAtomsState.test_value,
                    on_change=TestingAtomsState.validate_input
                ),
                rx.text(f"Valor actual: {TestingAtomsState.test_value}", color="gray"),
                spacing="2"
            ),
            
            rx.divider(margin_y="20px"),
            
            rx.heading("Badges / Validadores", size="6", margin_bottom="10px"),
            rx.hstack(
                badge("Validación en tiempo real", TestingAtomsState.is_valid),
                spacing="4"
            ),
            
            rx.divider(margin_y="20px"),
            
            rx.heading("Toasts", size="6", margin_bottom="10px"),
            rx.vstack(
                button("Mostrar Toast (rx.toast)", on_click=TestingAtomsState.show_toast),
                rx.text("Haz clic para probar los Toasts Atómicos y personalizables:"),
                button("Custom Toast General", on_click=toast("Registro exitoso", bg_color=rx.color_mode_cond(light="#5a228b", dark="#ffffff"), color=rx.color_mode_cond(light="white", dark="#5a228b"), close_button=True)),
                button("Operación exitosa", on_click=toast.success("Operación exitosa",)),
                button("Error en operación", on_click=toast.error("Ha ocurrido un error")),
                button("Advertencia", on_click=toast.warning("Ten cuidado con esta acción")),
                button("Información", on_click=toast.info("Este es un mensaje informativo")),
                spacing="4",
                align_items="flex-start"
            ),
            
            rx.divider(margin_y="20px"),
            
            rx.heading("Alert Dialogs", size="6", margin_bottom="10px"),
            alert_dialog(
                title="Alerta de prueba",
                description="Puedes usarla para confirmar acciones destructivas.",
            ),
            dialog(
                title="Diálogo de prueba",
                description="Este es un diálogo más genérico, sin opciones de confirmación específicas.",
            ),
            
            padding="40px",
            max_width="800px",
            margin="0 auto",
            align_items="stretch"
        ),
        min_height="100vh",
        background_color="var(--gray-1)",
        color="var(--gray-12)"
    )
