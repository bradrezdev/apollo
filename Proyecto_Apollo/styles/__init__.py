"""__init__.py para estilos - Punto central de importación"""

from . import colors
from . import chat_styles
from . import sidebar_styles
from . import header_styles
from . import common_styles

# Exportar todo para facilitar importaciones
__all__ = [
    "colors",
    "chat_styles",
    "sidebar_styles",
    "header_styles",
    "common_styles",
]
