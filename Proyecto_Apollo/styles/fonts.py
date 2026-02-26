"""
Sistema de tipografía oficial - ONANO
Basado en design_system_ONANO.md
"""

# --- FAMILIAS TIPOGRÁFICAS ---
FONT_FAMILY_PRIMARY = "Avenir Next, system-ui, sans-serif"
FONT_FAMILY_SUPPORT = "Poppins, sans-serif"

# Alias para uso general
FONT_FAMILY = FONT_FAMILY_PRIMARY
FONT_FAMILY_BODY = FONT_FAMILY_PRIMARY # Según design system, Avenir Next es la principal

# --- PESOS ---
WEIGHT_REGULAR = "400"
WEIGHT_MEDIUM = "500"
WEIGHT_SEMIBOLD = "600"
WEIGHT_BOLD = "700"

# --- TAMAÑOS (ESCALA TIPOGRÁFICA) ---
SIZE_DISPLAY = "34px"        # Hero principal
SIZE_H1 = "24px"             # Título de página
SIZE_H2 = "20px"             # Encabezados de sección
SIZE_H3 = "17px"             # Tarjetas
SIZE_CTA = "17px"            # Botón principal
SIZE_BODY = "16px"           # Texto base / Botón secundario
SIZE_COMPACT = "15px"        # Texto reducido
SIZE_LABEL = "14px"          # Inputs / Labels
SIZE_BADGE = "13px"          # Status / Tags
SIZE_MICRO = "12px"          # Legal / Footer

# --- LETTER SPACING (KERNING) ---
KERNING_WIDE = "0.5px"       # Para Label, Badge, Micro

# --- ESTILOS PREDEFINIDOS (Mixins) ---
# Dicccionarios listos para usar en componentes rx.text(style=STYLE_NAME)

STYLE_DISPLAY = {
    "font_family": FONT_FAMILY_PRIMARY,
    "font_size": SIZE_DISPLAY,
    "font_weight": WEIGHT_BOLD,
    "line_height": "1.2",
}

STYLE_H1 = {
    "font_family": FONT_FAMILY_PRIMARY,
    "font_size": SIZE_H1,
    "font_weight": WEIGHT_BOLD,
    "line_height": "1.3",
}

STYLE_H2 = {
    "font_family": FONT_FAMILY_PRIMARY,
    "font_size": SIZE_H2,
    "font_weight": WEIGHT_SEMIBOLD,
    "line_height": "1.4",
}

STYLE_H3 = {
    "font_family": FONT_FAMILY_PRIMARY,
    "font_size": SIZE_H3,
    "font_weight": WEIGHT_SEMIBOLD,
    "line_height": "1.4",
}

STYLE_CTA = {
    "font_family": FONT_FAMILY_PRIMARY,
    "font_size": SIZE_CTA,
    "font_weight": WEIGHT_SEMIBOLD,
    "line_height": "1.2",
}

STYLE_BODY = {
    "font_family": FONT_FAMILY_BODY,
    "font_size": SIZE_BODY,
    "font_weight": WEIGHT_REGULAR,
    "line_height": "1.6",
}

STYLE_LABEL = {
    "font_family": FONT_FAMILY_SUPPORT, # Usamos fuente de soporte para UI elements
    "font_size": SIZE_LABEL,
    "font_weight": WEIGHT_MEDIUM,
    "letter_spacing": KERNING_WIDE,
    "text_transform": "uppercase",
}

STYLE_BADGE = {
    "font_family": FONT_FAMILY_SUPPORT, # Usamos fuente de soporte para UI elements
    "font_size": SIZE_BADGE,
    "font_weight": WEIGHT_MEDIUM,
    "letter_spacing": KERNING_WIDE,
    "text_transform": "uppercase",
}

STYLE_MICRO = {
    "font_family": FONT_FAMILY_SUPPORT,
    "font_size": SIZE_MICRO,
    "font_weight": WEIGHT_REGULAR,
    "letter_spacing": KERNING_WIDE,
}