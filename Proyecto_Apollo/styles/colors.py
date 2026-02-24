"""Sistema de colores temáticos para Apollo basado en Design System ONANO v2.0"""

import reflex as rx

# === PALETA OFICIAL ONANO ===

# Color Primario (Azul Profundo) - Estabilidad, Ciencia
PRIMARY_100 = "#062A63"
PRIMARY_80 = "#355078"
PRIMARY_60 = "#677C9A"
PRIMARY_40 = "#9AA7BB"
PRIMARY_20 = "#CCD3DD"

# Color Secundario (Azul Tecnológico) - Innovación
SECONDARY_100 = "#0CBCE5"
SECONDARY_80 = "#3DC9EA"
SECONDARY_60 = "#6DD7EF"
SECONDARY_40 = "#9EE4F5"
SECONDARY_20 = "#CEF2FA"

# Neutrales & Fondos
NEUTRAL_WHITE = "#FFFFFF"
NEUTRAL_SOFT_BG = "#F2F4F9"
NEUTRAL_TEXT_DARK = "#383A3F"
NEUTRAL_BORDER = "#EAECF0" # Separadores suaves
NEUTRAL_GRAY_100 = "#F0F0F0"

# Feedback Colors (Estándar, adaptados si es necesario)
SUCCESS = "#10B981"
WARNING = "#F59E0B"
ERROR = "#EF4444"
INFO = "#3B82F6"


class ColorSystem:
    """Acceso rápido a colores del sistema"""
    PRIMARY = PRIMARY_100
    SECONDARY = SECONDARY_100
    BACKGROUND = NEUTRAL_SOFT_BG
    TEXT = NEUTRAL_TEXT_DARK
    WHITE = NEUTRAL_WHITE
    BORDER = NEUTRAL_BORDER


class ApolloTheme:
    """Clase que contiene los colores del tema para Apollo"""
    
    @staticmethod
    def light_colors():
        """Colores para el modo claro (Principal ONANO)"""
        return {
            # === COLORES PRINCIPALES ===
            "primary": PRIMARY_100,
            "secondary": SECONDARY_100,
            "accent": SECONDARY_100,
            
            # === FONDOS ===
            "background_color": NEUTRAL_SOFT_BG,     # #F2F4F9
            "secondary_background": NEUTRAL_WHITE,   # #FFFFFF
            "translucid_background": "rgba(255, 255, 255, 0.85)", # Glassmorphism
            
            # === SIDEBAR ===
            "sidebar_background": PRIMARY_100,       # #062A63 (Azul Profundo para sidebar)
            "sidebar_text_color": "#FFFFFF",
            "sidebar_button_color": "rgba(255, 255, 255, 0.1)",
            "sidebar_button_hover_color": SECONDARY_100,
            "sidebar_item_hover": SECONDARY_100,
            
            # === HEADER ===
            "header_background": NEUTRAL_WHITE,
            "header_text_color": PRIMARY_100,
            "header_icon_color": PRIMARY_100,
            
            # === CHAT ===
            "question_background": PRIMARY_100,      # Mensaje usuario (Azul Profundo)
            "question_text_color": "#FFFFFF",
            "answer_background": "transparent",
            "answer_text_color": NEUTRAL_TEXT_DARK,  # #383A3F
            
            # === BOTONES ===
            "new_chat_color": SECONDARY_100,         # CTA
            "new_chat_hover_color": SECONDARY_80,
            "send_button_color": PRIMARY_100,
            "send_button_hover_color": PRIMARY_80,
            "delete_button_color": ERROR,
            "delete_button_hover_color": "#DC2626",
            
            # === INPUT ===
            "input_background": NEUTRAL_WHITE,
            "input_border": NEUTRAL_BORDER,
            "input_text_color": NEUTRAL_TEXT_DARK,
            "input_placeholder_color": "#9CA3AF",
            
            # === ESTADOS ===
            "success": SUCCESS,
            "success_light": "#D1FAE5",
            "warning": WARNING,
            "warning_light": "#FEF3C7",
            "error": ERROR,
            "error_light": "#FEE2E2",
            "info": INFO,
            "info_light": "#DBEAFE",
            
            # === SOMBRAS Y EFECTOS ===
            "box_shadow": "0 4px 24px rgba(6, 42, 99, 0.08)", # Sombra con tinte azul
            "box_shadow_hover": "0 8px 32px rgba(6, 42, 99, 0.12)",
        }
    
    @staticmethod
    def dark_colors():
        """
        Colores para el modo oscuro.
        Aunque ONANO es light-first, mantenemos soporte dark mode adaptado.
        """
        return {
            # === COLORES PRINCIPALES ===
            "primary": PRIMARY_80,      # Un poco más claro en dark
            "secondary": SECONDARY_100, # Azul Tech brilla bien en dark
            "accent": SECONDARY_100,
            
            # === FONDOS ===
            "background_color": "#0B111A",           # Muy oscuro, casi negro azulado
            "secondary_background": "#151F2E",       # Gris azulado oscuro
            "translucid_background": "rgba(11, 17, 26, 0.85)",
            
            # === SIDEBAR ===
            "sidebar_background": "#051833",         # Versión más oscura del primario
            "sidebar_text_color": "#FFFFFF",
            "sidebar_button_color": "rgba(255, 255, 255, 0.05)",
            "sidebar_button_hover_color": SECONDARY_100,
            "sidebar_item_hover": SECONDARY_100,
            
            # === HEADER ===
            "header_background": "#151F2E",
            "header_text_color": "#FFFFFF",
            "header_icon_color": "#FFFFFF",
            
            # === CHAT ===
            "question_background": PRIMARY_60,       # Más suave para que no canse
            "question_text_color": "#FFFFFF",
            "answer_background": "transparent",
            "answer_text_color": "#E5E7EB",          # Gris claro para texto
            
            # === BOTONES ===
            "new_chat_color": SECONDARY_100,
            "new_chat_hover_color": SECONDARY_80,
            "send_button_color": SECONDARY_100,      # En dark mode el secundario resalta mejor
            "send_button_hover_color": SECONDARY_80,
            "delete_button_color": ERROR,
            "delete_button_hover_color": "#DC2626",
            
            # === INPUT ===
            "input_background": "#1F2937",
            "input_border": "#374151",
            "input_text_color": "#FFFFFF",
            "input_placeholder_color": "#6B7280",
            
            # === ESTADOS ===
            "success": "#34D399",
            "success_light": "rgba(16, 185, 129, 0.2)",
            "warning": "#FBBF24",
            "warning_light": "rgba(245, 158, 11, 0.2)",
            "error": "#F87171",
            "error_light": "rgba(239, 68, 68, 0.2)",
            "info": "#60A5FA",
            "info_light": "rgba(59, 130, 246, 0.2)",
            
            # === SOMBRAS Y EFECTOS ===
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.5)",
            "box_shadow_hover": "0 6px 16px rgba(0, 0, 0, 0.7)",
        }
