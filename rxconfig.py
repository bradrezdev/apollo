import reflex as rx
from Proyecto_Apollo.config.settings import APP_NAME, DATABASE_URL, SUPABASE_URL, SUPABASE_ANON_KEY

config = rx.Config(
    app_name=APP_NAME,
    db_url=DATABASE_URL,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    state_auto_setters=True,
    suplex={
        "api_url": SUPABASE_URL,
        "api_key": SUPABASE_ANON_KEY,
        # jwt_secret removido: el proyecto usa JWT Keys ECC (P-256) / ES256.
        # Suplex decodifica con JWKS cuando jwt_secret no está presente.
        # Ver: https://supabase.com/docs/guides/auth/jwts
        "cookie_max_age": 60 * 60 * 24 * 7,  # 7 días
        "debug": True,
    },
)