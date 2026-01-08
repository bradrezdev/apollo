import reflex as rx
from Proyecto_Apollo.config.settings import APP_NAME, DATABASE_URL

config = rx.Config(
    app_name=APP_NAME,
    # db_url=DATABASE_URL,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    state_auto_setters=True,
)