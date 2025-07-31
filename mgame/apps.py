from django.apps import AppConfig


class MgameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mgame"

    def ready(self):
        import mgame.signals