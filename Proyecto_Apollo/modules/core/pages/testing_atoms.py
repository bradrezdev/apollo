import reflex as rx
from Proyecto_Apollo.components.ui import atom_button, atom_input, atom_badge, atom_toast, atom_alert_dialog

class TestingAtomsState(rx.State):
    """Estado para la página de testing de átomos."""
    test_value: str = ""
    is_valid: bool = False
    
    def validate_input(self, value: str):
        self.test_value = value
        self.is_valid = len(value) > 3
        
    def show_toast(self):
        return rx.toast("Esto es un Toast de prueba desde el state", position="bottom-right")

def testing_atoms_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Página de Testing - Átomos UI", size="8", margin_bottom="20px"),
            rx.text("Aquí se encuentran todos los componentes 'átomo' para editar su estilo base y que se replique en todo el proyecto."),
            
            rx.divider(margin_y="20px"),
            
            rx.heading("Botones", size="6", margin_bottom="10px"),
            rx.hstack(
                atom_button("Primary Button", variant="primary", width="200px"),
                atom_button("Outline Button", variant="outline", width="200px"),
                atom_button("Ghost Button", variant="ghost", width="200px"),
                spacing="4"
            ),
            
            rx.divider(margin_y="20px"),
            
            rx.heading("Inputs", size="6", margin_bottom="10px"),
            rx.vstack(
                atom_input(
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
                atom_badge("Validación en tiempo real", is_valid=TestingAtomsState.is_valid),
                spacing="4"
            ),
            
            rx.divider(margin_y="20px"),
            
            rx.heading("Toasts", size="6", margin_bottom="10px"),
            rx.vstack(
                rx.button("Mostrar Toast (rx.toast)", on_click=TestingAtomsState.show_toast),
                rx.text("UI del Toast Atómico (para maquetación/referencia):"),
                atom_toast("Operación exitosa", type="success"),
                atom_toast("Aviso de información", type="info"),
                atom_toast("Ha ocurrido un error", type="error"),
                spacing="4",
                align_items="flex-start"
            ),
            
            rx.divider(margin_y="20px"),
            
            rx.heading("Alert Dialogs", size="6", margin_bottom="10px"),
            atom_alert_dialog(
                title="Alerta de prueba",
                description="Puedes usarla para confirmar acciones destructivas.",
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
