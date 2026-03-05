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
        "debug": _is_dev,
    },
)

# ── Monkey-patch: Suplex cookies con secure=False en desarrollo ──────────
# Suplex v0.2.7 hardcodea secure=True en las cookies access_token y refresh_token.
# En desarrollo (http://localhost) el browser NO envía cookies con secure=True,
# lo que causa que F5 pierda la sesión. Este override resuelve eso sin forkear Suplex.
# En producción (HTTPS), secure=True se mantiene para seguridad.
from suplex import Suplex  # noqa: E402

Suplex.access_token = rx.Cookie(
    name="access_token",
    path="/",
    secure=not _is_dev,
    same_site="lax",
    domain=None,
    max_age=_cookie_max_age,
)
Suplex.refresh_token = rx.Cookie(
    name="refresh_token",
    path="/",
    secure=not _is_dev,
    same_site="lax",
    domain=None,
    max_age=_cookie_max_age,
)