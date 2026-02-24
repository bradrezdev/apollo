"""Sistema de tipografía y fuentes para Apollo basado en Design System ONANO v2.0"""

class FontSystem:
    """Definición de familias y pesos tipográficos"""
    
    # Fuentes
    PRIMARY_FONT = "Avenir Next, system-ui, sans-serif" # Títulos, Headers
    SECONDARY_FONT = "Poppins, system-ui, sans-serif"   # Cuerpos, UI
    
    # Tamaños (Escala flexible)
    SIZE_DISPLAY = "34px"       # Hero Principal
    SIZE_H1 = "24px"           # Título Página
    SIZE_H2 = "20px"           # Encabezados Sección
    SIZE_H3 = "17px"           # Tarjetas / CTA
    SIZE_BODY = "16px"         # Texto base
    SIZE_BODY_COMPACT = "15px" # Texto reducido
    SIZE_LABEL = "14px"        # Labels
    SIZE_BADGE = "13px"        # Badges
    SIZE_MICRO = "12px"        # Legal / Microcopy
    
    # Pesos
    WEIGHT_BOLD = "700"
    WEIGHT_SEMIBOLD = "600"
    WEIGHT_MEDIUM = "500"
    WEIGHT_REGULAR = "400"

font_styles = {
    "font_family": FontSystem.SECONDARY_FONT,
    "heading_font_family": FontSystem.PRIMARY_FONT,
}
