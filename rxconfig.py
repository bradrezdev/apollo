import reflex as rx
from Proyecto_Apollo.config.settings import APP_NAME, DATABASE_URL, SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_JWT_SECRET

config = rx.Config(
    app_name=APP_NAME,
    db_url=DATABASE_URL,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    state_auto_setters=True,
    suplex={
        "api_url": SUPABASE_URL,
        "api_key": SUPABASE_ANON_KEY,
        "jwt_secret": SUPABASE_JWT_SECRET,
        "cookie_max_age": 60 * 60 * 24 * 7,  # 7 días
        "debug": True,
    },
)