import os
import reflex as rx
from Proyecto_Apollo.config.settings import APP_NAME, DATABASE_URL, SUPABASE_URL, SUPABASE_ANON_KEY

# Detectar si estamos en desarrollo (HTTP) o producción (HTTPS)
_is_dev = os.getenv("REFLEX_ENV", "dev").lower() in ("dev", "development", "local")
_cookie_max_age = 60 * 60 * 24 * 7  # 7 días

config = rx.Config(
    app_name=APP_NAME,
    db_url=DATABASE_URL,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    state_auto_setters=True,
    suplex={
        "api_url": SUPABASE_URL,
        "api_key": SUPABASE_ANON_KEY,
        # jwt_secret: valor placeholder requerido por Suplex v0.2.7 en __init__ cuando
        # _need_jwt_secret=True (se activa porque el anon key empieza con "eyJ", no "sb_publishable").
        # El proyecto usa JWT Keys ECC (P-256) / ES256 — este valor NUNCA se usa en runtime.
        # sign_in_user lee el UID desde la respuesta HTTP, sync_user_sync usa get_user() API,
        # y el auth guard verifica access_token (cookie), no claims decodificadas con HS256.
        # Ver: suplex.py línea 642-649 (startup validation) y línea 663-696 (claims computed var).
        "jwt_secret": "placeholder-not-used-project-uses-ecc-p256-es256",
        "cookie_max_age": _cookie_max_age,
        # cookie_secure: False en desarrollo (http://localhost) para que el browser acepte
        # las cookies de sesión. Los browsers rechazan silenciosamente cookies con Secure=True
        # en conexiones HTTP planas, lo que causaba pérdida de sesión en cada F5.
        # En producción (HTTPS) se mantiene True para seguridad.
        # NOTA: este valor es leído por suplex.py en el class body de Suplex (antes de que
        # Pydantic congele el schema), gracias al parche en .venv/suplex/suplex.py.
        # Si se reinstala suplex, re-aplicar el parche con: make patch-suplex
        "cookie_secure": not _is_dev,
        "debug": _is_dev,
    },
)