"""Sistema de colores temáticos para Apollo - Light & Dark Mode"""

import reflex as rx


class ApolloTheme:
    """Clase que contiene los colores del tema para Apollo"""
    
    @staticmethod
    def light_colors():
        """Colores para el modo claro"""
        return {
            # === COLORES PRINCIPALES ===
            "primary": "#0080ff",
            "secondary": "#5E79FF",
            "accent": "#0080ff",
            
            # === FONDOS ===
            "background_color": "#FFFFFF",
            "secondary_background": "#F2F3F8",
            "translucid_background": "rgba(255, 255, 255, 0.35)",
            
            # === SIDEBAR ===
            "sidebar_background": "#FFFFFF",
            "sidebar_button_color": "#FFFFFF",
            "sidebar_button_hover_color": rx.color("accent", 4),
            "sidebar_item_hover": rx.color("accent", 4),
            
            # === HEADER ===
            "header_background": "rgba(25, 25, 25, 0.35)",
            "header_text_color": "#FFFFFF",
            "header_icon_color": "#FFFFFF",
            
            # === CHAT ===
            "question_background": "#595959",
            "question_text_color": "#FFFFFF",
            "answer_background": "transparent",
            "answer_text_color": "#000000",
            
            # === BOTONES ===
            "new_chat_color": "#FFFFFF",
            "new_chat_hover_color": "rgba(255, 255, 255, 0.8)",
            "send_button_color": "#0080ff",
            "send_button_hover_color": "#0066cc",
            "delete_button_color": "#EF4444",
            "delete_button_hover_color": "#DC2626",
            
            # === INPUT ===
            "input_background": "rgba(255, 255, 255, 0.35)",
            "input_border": "#E5E7EB",
            "input_text_color": "#000000",
            "input_placeholder_color": "#9CA3AF",
            
            # === ESTADOS ===
            "success": "#10B981",
            "success_light": "#D1FAE5",
            "warning": "#F59E0B",
            "warning_light": "#FEF3C7",
            "error": "#EF4444",
            "error_light": "#FEE2E2",
            "info": "#3B82F6",
            "info_light": "#DBEAFE",
            
            # === SOMBRAS Y EFECTOS ===
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
            "box_shadow_hover": "0 6px 16px rgba(0, 0, 0, 0.15)",
        }
    
    @staticmethod
    def dark_colors():
        """Colores para el modo oscuro"""
        return {
            # === COLORES PRINCIPALES ===
            "primary": "#0080ff",
            "secondary": "#5E79FF",
            "accent": "#0080ff",
            
            # === FONDOS ===
            "background_color": "#000000",
            "secondary_background": "#1C1C1E",
            "translucid_background": "rgba(0, 0, 0, 0.6)",
            
            # === SIDEBAR ===
            "sidebar_background": "#1C1C1E",
            "sidebar_button_color": "#2C2C2E",
            "sidebar_button_hover_color": "#3A3A3C",
            "sidebar_item_hover": "#3A3A3C",
            
            # === HEADER ===
            "header_background": "rgba(0, 0, 0, 0.6)",
            "header_text_color": "#FFFFFF",
            "header_icon_color": "#FFFFFF",
            
            # === CHAT ===
            "question_background": "#2C2C2E",
            "question_text_color": "#FFFFFF",
            "answer_background": "transparent",
            "answer_text_color": "#FFFFFF",
            
            # === BOTONES ===
            "new_chat_color": "#2C2C2E",
            "new_chat_hover_color": "#3A3A3C",
            "send_button_color": "#0080ff",
            "send_button_hover_color": "#0066cc",
            "delete_button_color": "#EF4444",
            "delete_button_hover_color": "#DC2626",
            
            # === INPUT ===
            "input_background": "rgba(0, 0, 0, 0.6)",
            "input_border": "#3A3A3C",
            "input_text_color": "#FFFFFF",
            "input_placeholder_color": "#9CA3AF",
            
            # === ESTADOS ===
            "success": "#10B981",
            "success_light": "#D1FAE5",
            "warning": "#F59E0B",
            "warning_light": "#FEF3C7",
            "error": "#EF4444",
            "error_light": "#FEE2E2",
            "info": "#3B82F6",
            "info_light": "#DBEAFE",
            
            # === SOMBRAS Y EFECTOS ===
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
            "box_shadow_hover": "0 6px 16px rgba(0, 0, 0, 0.4)",
        }


# === FUNCIÓN HELPER PARA OBTENER COLORES SEGÚN EL MODO ===
def get_color(color_name: str, mode: str = "light") -> str:
    """
    Obtiene un color específico según el modo (light/dark)
    
    Args:
        color_name: Nombre del color (ej: 'background_color', 'primary')
        mode: 'light' o 'dark'
    
    Returns:
        str: Valor del color
    """
    colors = ApolloTheme.light_colors() if mode == "light" else ApolloTheme.dark_colors()
    return colors.get(color_name, "#000000")


# === COLORES RÁPIDOS (MODO LIGHT POR DEFECTO) ===
# Estos se mantienen para compatibilidad con código existente
theme = ApolloTheme.light_colors()

# Acceso directo a colores comunes
PRIMARY_BG = theme["background_color"]
ACCENT_COLOR = theme["accent"]
ACCENT_LIGHT = theme["sidebar_item_hover"]
ACCENT_DARK = rx.color("accent", 11)
WHITE = "#FFFFFF"
BLUE_PRIMARY = theme["primary"]
GRAY_DARK = theme["question_background"]
BLACK = "#000000"

